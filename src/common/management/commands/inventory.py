# české komentáře schválně – ať se ti to dobře udržuje

import ast
from pathlib import Path
import inspect

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


DEFAULT_PROJECT_APPS = {
    "accounts", "audit", "availability", "common", "fleet", "pricing", "reservations"
}


def _iter_py_files(app_path: Path):
    """Najde Python soubory v appce (vynechá migrace, __pycache__)."""
    for p in app_path.rglob("*.py"):
        if "/migrations/" in str(p).replace("\\", "/"):
            continue
        if "__pycache__" in p.parts:
            continue
        yield p


def _parse_file_symbols(py_file: Path):
    """
    Statická analýza souboru:
    - top-level funkce
    - třídy
    - metody tříd
    - docstringy
    """
    text = py_file.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(py_file))

    out = {
        "functions": [],  # (name, doc_first_line)
        "classes": [],    # (name, doc_first_line, methods=[...])
    }

    def doc1(node):
        d = ast.get_docstring(node) or ""
        d = d.strip().splitlines()[0] if d.strip() else ""
        return d

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            out["functions"].append((node.name, doc1(node)))
        elif isinstance(node, ast.ClassDef):
            methods = []
            for b in node.body:
                if isinstance(b, ast.FunctionDef):
                    methods.append((b.name, doc1(b)))
            out["classes"].append((node.name, doc1(node), methods))

    return out


def _is_own_model_method(model_cls, name, obj) -> bool:
    """Jen metody definované přímo v model třídě (bez zděděných a auto věcí)."""
    if name.startswith("_"):
        return False
    if not callable(obj):
        return False
    # odfiltrujeme Django generované/ORM věci
    if name in {"DoesNotExist", "MultipleObjectsReturned"}:
        return False
    try:
        qual = getattr(obj, "__qualname__", "")
        return qual.startswith(model_cls.__name__ + ".")
    except Exception:
        return False


class Command(BaseCommand):
    help = "Vygeneruje inventář projektu: modely + (volitelně) serializers/views/services/permissions/urls."

    def add_arguments(self, parser):
        parser.add_argument("--app", type=str, default=None, help="Jen konkrétní app label (např. reservations)")
        parser.add_argument(
            "--layers",
            type=str,
            default="models,code",
            help="Čárkou oddělené vrstvy: models,code. code = statická analýza py souborů",
        )

    def handle(self, *args, **options):
        app_filter = options["app"]
        layers = {x.strip() for x in (options["layers"] or "").split(",") if x.strip()}

        lines = []
        lines.append(f"✅ DJANGO_SETTINGS_MODULE: {settings.SETTINGS_MODULE}")
        lines.append(f"✅ DB ENGINE: {settings.DATABASES.get('default', {}).get('ENGINE')}")
        lines.append(f"✅ DB HOST: {settings.DATABASES.get('default', {}).get('HOST')}")
        lines.append(f"✅ DB NAME: {settings.DATABASES.get('default', {}).get('NAME')}")
        lines.append("")

        # 1) MODELS layer (Django runtime, přes apps.get_models())
        if "models" in layers:
            for model in apps.get_models():
                app_label = model._meta.app_label

                # jen naše appky + volitelně filtr
                if app_label not in DEFAULT_PROJECT_APPS:
                    continue
                if app_filter and app_label != app_filter:
                    continue

                lines.append(f"## {app_label}.{model.__name__}\n")

                lines.append("### Fields")
                for f in model._meta.get_fields():
                    if getattr(f, "auto_created", False) and not getattr(f, "concrete", False):
                        continue
                    name = getattr(f, "name", str(f))
                    ftype = f.__class__.__name__
                    null = getattr(f, "null", None)
                    blank = getattr(f, "blank", None)
                    unique = getattr(f, "unique", None)
                    lines.append(f"- `{name}` ({ftype}) null={null} blank={blank} unique={unique}")

                # properties definované na třídě
                lines.append("\n### Properties")
                props = []
                for name, obj in model.__dict__.items():
                    if isinstance(obj, property) and not name.startswith("_"):
                        props.append(name)
                if props:
                    for p in sorted(props):
                        lines.append(f"- `{p}` (property)")
                else:
                    lines.append("- (žádné)")

                # vlastní metody
                lines.append("\n### Methods")
                methods = []
                for name, obj in inspect.getmembers(model):
                    if _is_own_model_method(model, name, obj):
                        methods.append(name)
                if methods:
                    for m in sorted(set(methods)):
                        doc = getattr(getattr(model, m), "__doc__", None) or ""
                        doc_line = doc.strip().splitlines()[0] if doc.strip() else ""
                        lines.append(f"- `{m}()`" + (f" – {doc_line}" if doc_line else ""))
                else:
                    lines.append("- (žádné)")

                lines.append("")

        # 2) CODE layer (statická analýza .py souborů v appkách)
        if "code" in layers:
            # najdeme fyzické cesty appek podle INSTALLED_APPS
            for app_label in DEFAULT_PROJECT_APPS:
                if app_filter and app_label != app_filter:
                    continue

                # zkusíme najít složku appky v BASE_DIR/src
                base = Path(settings.BASE_DIR)
                # u tebe je projekt pod /workspace/src, takže BASE_DIR bude nejspíš /workspace/src
                app_path = base / app_label
                if not app_path.exists():
                    continue

                lines.append(f"# Code inventory: {app_label}\n")

                for py_file in sorted(_iter_py_files(app_path)):
                    rel = py_file.relative_to(base)
                    symbols = _parse_file_symbols(py_file)

                    # filtr: chceme hlavně vrstvy
                    is_interesting = any(
                        x in rel.as_posix()
                        for x in ("views.py", "serializers.py", "permissions.py", "services.py", "urls.py")
                    )
                    if not is_interesting:
                        continue

                    lines.append(f"## {rel.as_posix()}\n")

                    if symbols["classes"]:
                        lines.append("### Classes")
                        for cls_name, cls_doc, methods in symbols["classes"]:
                            lines.append(f"- `{cls_name}`" + (f" – {cls_doc}" if cls_doc else ""))
                            for m_name, m_doc in methods:
                                if m_name.startswith("_"):
                                    continue
                                lines.append(f"  - `{m_name}()`" + (f" – {m_doc}" if m_doc else ""))

                    if symbols["functions"]:
                        lines.append("\n### Functions")
                        for fn_name, fn_doc in symbols["functions"]:
                            if fn_name.startswith("_"):
                                continue
                            lines.append(f"- `{fn_name}()`" + (f" – {fn_doc}" if fn_doc else ""))

                    lines.append("")

        self.stdout.write("\n".join(lines))
import ast
from pathlib import Path
import inspect

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


DEFAULT_PROJECT_APPS = {
    "accounts", "audit", "availability", "common", "fleet", "pricing", "reservations"
}


def _iter_py_files(app_path: Path):
    """Najde Python soubory v appce (vynechá migrace, __pycache__)."""
    for p in app_path.rglob("*.py"):
        if "/migrations/" in str(p).replace("\\", "/"):
            continue
        if "__pycache__" in p.parts:
            continue
        yield p


def _parse_file_symbols(py_file: Path):
    """
    Statická analýza souboru:
    - top-level funkce
    - třídy
    - metody tříd
    - docstringy
    """
    text = py_file.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(py_file))

    out = {
        "functions": [],  # (name, doc_first_line)
        "classes": [],    # (name, doc_first_line, methods=[...])
    }

    def doc1(node):
        d = ast.get_docstring(node) or ""
        d = d.strip().splitlines()[0] if d.strip() else ""
        return d

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            out["functions"].append((node.name, doc1(node)))
        elif isinstance(node, ast.ClassDef):
            methods = []
            for b in node.body:
                if isinstance(b, ast.FunctionDef):
                    methods.append((b.name, doc1(b)))
            out["classes"].append((node.name, doc1(node), methods))

    return out


def _is_own_model_method(model_cls, name, obj) -> bool:
    """Jen metody definované přímo v model třídě (bez zděděných a auto věcí)."""
    if name.startswith("_"):
        return False
    if not callable(obj):
        return False
    # odfiltrujeme Django generované/ORM věci
    if name in {"DoesNotExist", "MultipleObjectsReturned"}:
        return False
    try:
        qual = getattr(obj, "__qualname__", "")
        return qual.startswith(model_cls.__name__ + ".")
    except Exception:
        return False


class Command(BaseCommand):
    help = "Vygeneruje inventář projektu: modely + (volitelně) serializers/views/services/permissions/urls."

    def add_arguments(self, parser):
        parser.add_argument("--app", type=str, default=None, help="Jen konkrétní app label (např. reservations)")
        parser.add_argument(
            "--layers",
            type=str,
            default="models,code",
            help="Čárkou oddělené vrstvy: models,code. code = statická analýza py souborů",
        )

    def handle(self, *args, **options):
        app_filter = options["app"]
        layers = {x.strip() for x in (options["layers"] or "").split(",") if x.strip()}

        lines = []
        lines.append(f"✅ DJANGO_SETTINGS_MODULE: {settings.SETTINGS_MODULE}")
        lines.append(f"✅ DB ENGINE: {settings.DATABASES.get('default', {}).get('ENGINE')}")
        lines.append(f"✅ DB HOST: {settings.DATABASES.get('default', {}).get('HOST')}")
        lines.append(f"✅ DB NAME: {settings.DATABASES.get('default', {}).get('NAME')}")
        lines.append("")

        # 1) MODELS layer (Django runtime, přes apps.get_models())
        if "models" in layers:
            for model in apps.get_models():
                app_label = model._meta.app_label

                # jen naše appky + volitelně filtr
                if app_label not in DEFAULT_PROJECT_APPS:
                    continue
                if app_filter and app_label != app_filter:
                    continue

                lines.append(f"## {app_label}.{model.__name__}\n")

                lines.append("### Fields")
                for f in model._meta.get_fields():
                    if getattr(f, "auto_created", False) and not getattr(f, "concrete", False):
                        continue
                    name = getattr(f, "name", str(f))
                    ftype = f.__class__.__name__
                    null = getattr(f, "null", None)
                    blank = getattr(f, "blank", None)
                    unique = getattr(f, "unique", None)
                    lines.append(f"- `{name}` ({ftype}) null={null} blank={blank} unique={unique}")

                # properties definované na třídě
                lines.append("\n### Properties")
                props = []
                for name, obj in model.__dict__.items():
                    if isinstance(obj, property) and not name.startswith("_"):
                        props.append(name)
                if props:
                    for p in sorted(props):
                        lines.append(f"- `{p}` (property)")
                else:
                    lines.append("- (žádné)")

                # vlastní metody
                lines.append("\n### Methods")
                methods = []
                for name, obj in inspect.getmembers(model):
                    if _is_own_model_method(model, name, obj):
                        methods.append(name)
                if methods:
                    for m in sorted(set(methods)):
                        doc = getattr(getattr(model, m), "__doc__", None) or ""
                        doc_line = doc.strip().splitlines()[0] if doc.strip() else ""
                        lines.append(f"- `{m}()`" + (f" – {doc_line}" if doc_line else ""))
                else:
                    lines.append("- (žádné)")

                lines.append("")

        # 2) CODE layer (statická analýza .py souborů v appkách)
        if "code" in layers:
            # najdeme fyzické cesty appek podle INSTALLED_APPS
            for app_label in DEFAULT_PROJECT_APPS:
                if app_filter and app_label != app_filter:
                    continue

                # zkusíme najít složku appky v BASE_DIR/src
                base = Path(settings.BASE_DIR)
                # u tebe je projekt pod /workspace/src, takže BASE_DIR bude nejspíš /workspace/src
                app_path = base / app_label
                if not app_path.exists():
                    continue

                lines.append(f"# Code inventory: {app_label}\n")

                for py_file in sorted(_iter_py_files(app_path)):
                    rel = py_file.relative_to(base)
                    symbols = _parse_file_symbols(py_file)

                    # filtr: chceme hlavně vrstvy
                    is_interesting = any(
                        x in rel.as_posix()
                        for x in ("views.py", "serializers.py", "permissions.py", "services.py", "urls.py")
                    )
                    if not is_interesting:
                        continue

                    lines.append(f"## {rel.as_posix()}\n")

                    if symbols["classes"]:
                        lines.append("### Classes")
                        for cls_name, cls_doc, methods in symbols["classes"]:
                            lines.append(f"- `{cls_name}`" + (f" – {cls_doc}" if cls_doc else ""))
                            for m_name, m_doc in methods:
                                if m_name.startswith("_"):
                                    continue
                                lines.append(f"  - `{m_name}()`" + (f" – {m_doc}" if m_doc else ""))

                    if symbols["functions"]:
                        lines.append("\n### Functions")
                        for fn_name, fn_doc in symbols["functions"]:
                            if fn_name.startswith("_"):
                                continue
                            lines.append(f"- `{fn_name}()`" + (f" – {fn_doc}" if fn_doc else ""))

                    lines.append("")

        self.stdout.write("\n".join(lines))

# Dokumentace
- Viz docs/README.md

## Inventory
- [Inventory v2 (aktuální)](inventory/v2/INDEX.md)
- Inventory v1 (archiv) – bude doplněno

## Diagramy
Architektura a doménový model jsou dokumentovány pomocí PlantUML.

Zdrojové soubory:
- `docs/diagrams/*.puml`

Vygenerované výstupy:
- `docs/diagrams/*.svg`
- `docs/diagrams/*.png`


Excel: CAR_RESERVATION_DataDictionary_v9_inventory_gaps_targets_rationale.xlsx

Tento Excel je centrální specifikace + kontrolní checklist pro projekt CAR-RESERVATION. Slouží jako „single source of truth“ pro:
    - DB datový slovník (modely, atributy, typy, účel, omezení)
    - ne-DB pravidla (API konvence, timezones, error contract, idempotence, cron…)
    - metody a call-flow (kde se metoda spouští a co volá dál)
    - komparaci proti INVENTORY.md souborům (coverage a mezery)

Obsah (hlavní listy)
1) Datový slovník (DB)
Samostatné listy pro modely:
    Reservation, ReservationEvent, Vehicle, AvailabilityBlock
    CustomerProfile, StaffProfile
    Branch, Fleet, Region

Každý list obsahuje sloupce typu:
    Model / Atribut / Typ / Účel / Poznámky a omezení
(tj. co pole znamená, proč existuje, co validovat, co je “sporné pole”, atd.)
    List All_Models obsahuje všechny atributy ze všech modelů v jednom místě pro filtrování.

2) Non-DB pravidla (API & systémové konvence)
List Non_DB_Items popisuje věci, které nejsou v DB, ale jsou zásadní pro implementaci:
    - JWT headers a autentizace
    - Idempotency-Key a replay pravidla
    - X-Request-Id pro korelaci logů
    - pravidla pro datetime (ISO8601 s TZ offsetem, DB ukládá UTC)
    - error contract a HTTP sémantika (400/409/403/404)
    - pagination/filtering/ordering
    - cron expirace HOLD

3) Metody a call-flow (kde co běží a co volá)
Listy Methods_* (a agregovaný Methods_All) dokumentují metody po vrstvách:
    - Service layer (use-case metody typu confirm/cancel/pickup/return…)
    - Availability (overlap/blocks/buffer/working hours/warnings…)
    - StateMachine (apply_transition + guard evaluation)
    - API (viewset akce a mapování na endpointy)
    - Idempotency (uložení a replay odpovědi)
    - Audit/EventLogger (zápis ReservationEvent)

U metod je klíčové, že mají zároveň:
    - Voláno z (entrypoint) – odkud metoda startuje (API endpoint / cron / interně)
    - Volá (calls) – co metoda volá dál (kvůli orientaci a bezpečnému refaktoru)

4) Checklist + komparace proti INVENTORY.md
List Inventory_Checklist je master checklist všech položek:
    - atributy (DB)
    - metody (call-flow)
    - non-DB pravidla

Obsahuje sloupce:
    - V INVENTORY? (ANO/NE) a INVENTORY soubor, kde se položka našla

List Inventory_Gaps obsahuje pouze položky, které v INVENTORY chybí, včetně:
    - Doporučený cílový soubor (kam to dopsat, např. INVENTORY_reservations_FULL.md)
    - Proč tam patří (rationale) (odůvodnění – doména vs cross-cutting vs config vs audit)

Doporučené použití
    - Při změnách DB nebo logiky nejdřív upravit tento Excel (spec), potom až kód.
    - Při psaní/úpravách INVENTORY*.md použít Inventory_Gaps jako „todo list“.
    - Methods_All používat jako navigaci “kdo koho volá”, aby se business logika nerozlezla do viewsetů.

Doporučený workflow pro PR / commit (spec → kód → kontrola)
Cílem je mít minimum kolizí a vždy jasně vědět „kam sáhnout“ při změnách. Proto držíme pravidlo: nejdřív specifikace, potom implementace.
1) Klasifikuj změnu (co se mění?)
Před úpravou si řekni, do které kategorie změna patří:
    •	DB/Model změna (nové pole, změna typu, index, FK, constraints)
    •	Business logika / use-case (nová akce, změna guardu, změna state machine)
    •	API kontrakt (request/response, error code, HTTP status, pagination/filter)
    •	Cross-cutting (idempotence, audit/logování, timezone pravidla)
    •	Konfigurace (routing /api/v1, JWT, cron, devcontainer…)
To určuje, které soubory se musí aktualizovat.
________________________________________
2) Aktualizuj SPEC (Excel) jako první krok
Před tím, než sáhneš do kódu:
    •	uprav relevantní listy v Excelu:
        o	DB: konkrétní model sheet + All_Models
        o	Non-DB: Non_DB_Items
        o	Metody/call-flow: Methods_* + Methods_All
    o	Checklist: Inventory_Checklist (pokud přidáváš novou položku)
    •	pokud vzniká nový bod k dokumentaci, přidej ho tak, aby se objevil i v checklistu (tzn. aby byl          kontrolovatelný)
Praktický tip: změny v Excelu dělej v rámci stejného PR/commitu jako změny v kódu.
________________________________________
3) Aktualizuj INVENTORY.md (dokumentace k modulu)
Po změně specifikace (Excelu) dopsat dokumentaci:
    •	otevři Inventory_Gaps a řiď se sloupci:
        o	Doporučený cílový soubor
        o	Proč tam patří (rationale)
    •	doplň nebo uprav příslušný:
        o	INVENTORY_reservations_FULL.md (rezervace, akce, state machine)
        o	INVENTORY_availability_FULL.md (overlaps, buffer, working hours, tz pravidla)
        o	INVENTORY_audit_FULL.md (ReservationEvent, logování sporných polí)
        o	INVENTORY_common_FULL.md (idempotence, auth, shared error contract část)
        o	INVENTORY_config_FULL.md (routing, /api/v1, config zásady)
        o	INVENTORY_fleet_FULL.md, INVENTORY_accounts_FULL.md, INVENTORY_pricing_FULL.md…
________________________________________
4) Implementace v kódu (Django)
Teprve teď uprav kód:
    •	Models + migrations (Postgres):
        o	přidat pole / indexy / constraints dle Excelu
    •	Service layer:
        o	business logika patří do services, ne do viewsetů
    •	State machine + guardy:
        o	změny přechodů → změny guardů → změny error mapování
    •	Audit (ReservationEvent):
        o	sporná pole vždy logovat jako *_CHANGED event
    •	Idempotence:
        o	u POST /create a POST /actions vždy respektovat Idempotency-Key
________________________________________
5) Testy a “contract checks”
V PR by mělo být jasné, co se testuje:
    •	State machine:
        o	allowed transitions + forbidden transitions (guardy)
    •	Availability:
        o	overlap, blocks, buffer, timezone input
    •	Error contract:
        o	správný error.code + HTTP status (400 vs 409)
    •	Idempotence:
        o	stejný Idempotency-Key → stejná odpověď, žádný duplicitní event
    •	Audit:
        o	po změně sporného pole vznikne odpovídající ReservationEvent
________________________________________
6) Checklist před merge (Definition of Done)
V PR popisu odškrtni:
    •	Aktualizován Excel CAR_RESERVATION_DataDictionary...xlsx (relevantní listy)
    •	Aktualizován odpovídající INVENTORY_*_FULL.md
    •	Inventory_Gaps se nezhoršil (nebo je záměrně okomentováno proč)
    •	Implementace odpovídá “Methods_All” (business logika není ve viewsetech)
    •	Přidány/aktualizovány testy pro guardy, availability, error codes, idempotenci
    •	U sporných polí je audit event (ReservationEvent)
________________________________________
7) Doporučená struktura commitů
Aby se v historii dobře hledalo:
    1.	spec: aktualizace Excel + INVENTORY
    2.	feat/fix: změny v kódu (models/services/api)
    3.	test: testy + případně docs drobnosti
Příklad názvů:
•	spec(reservations): add hold_expires_at + confirm guard rules
•	feat(reservations): implement confirm flow with idempotency + audit
•	test(reservations): cover confirm conflict + overlap + idempotency replay
________________________________________
8) Jak řešit budoucí rozvoj bez chaosu
Když budeš chtít něco rozšířit (např. platby, fotodokumentace, více poboček pickup/return):
    •	nejdřív přidej nové položky do Excelu (DB + metody + non-DB)
    •	podívej se do Methods_All, kde se to “napojí”
    •	doplň INVENTORY do doporučeného souboru
    
    •	až pak kód


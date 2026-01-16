FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends cron curl \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.3
RUN pip install "poetry==${POETRY_VERSION}"

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

WORKDIR /workspace

COPY docker/cron/entrypoint.sh /entrypoint.sh
COPY docker/cron/crontab /etc/cron.d/car-cron

RUN chmod +x /entrypoint.sh \
 && chmod 0644 /etc/cron.d/car-cron \
 && crontab /etc/cron.d/car-cron \
 && touch /var/log/cron.log

CMD ["/entrypoint.sh"]

FROM python:3.8-slim
LABEL maintainer="Anton Lebedev <mailbox@lebster.me>"

RUN apt-get update && \
  apt-get --no-install-recommends --assume-yes install curl

RUN pip install pipenv
COPY dummy_bot/Pipfile* /tmp/
RUN cd /tmp \
    && pipenv lock --requirements > requirements.txt \
    && pip install -r /tmp/requirements.txt

COPY dummy_bot /srv/dummy_bot
WORKDIR /

ENV TELEGRAM_API_TOKEN=${TELEGRAM_API_TOKEN}
HEALTHCHECK --interval=30s --timeout=30s --start-period=1ms --retries=3 \
    CMD curl --fail https://api.telegram.org/bot${TELEGRAM_API_TOKEN}/getWebhookInfo || exit 1

CMD python /srv/dummy_bot/bot.py

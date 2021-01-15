FROM python:3.8-slim
LABEL maintainer="Anton Lebedev <mailbox@lebster.me>"

RUN pip install pipenv
COPY dummy_bot/Pipfile* /tmp/
RUN cd /tmp \
    && pipenv lock --requirements > requirements.txt \
    && pip install -r /tmp/requirements.txt

COPY dummy_bot /srv/dummy_bot
WORKDIR /
CMD python /srv/dummy_bot/bot.py

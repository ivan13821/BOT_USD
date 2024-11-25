FROM python:3.10-slim AS bot

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

# Env vars
# ENV TELEGRAM_TOKEN ${TELEGRAM_TOKEN}


RUN apt-get clean && apt-get update
RUN pip install --upgrade pip

RUN apt-get install -y python3 python3-pip python3-venv

RUN apt update

RUN apt-get update
RUN apt-get install -y python3-dev libpq-dev
RUN export PATH=$PATH:/path/to/pg_config
RUN pip install psycopg2-binary
RUN pip install psycopg2

RUN apt-get install libpq-dev

WORKDIR /

RUN apt update

COPY requirements.txt requirements.txt
COPY game_for_economists/ game_for_economists/
COPY keyboard_factory/ keyboard_factory/
COPY other/ other/
COPY config.ini config.ini
COPY StopSpamMidleware.py StopSpamMidleware.py
COPY config.py config.py 
COPY bot_start.py bot_start.py

RUN apt update

RUN pip install -r requirements.txt
RUN chmod +x /bot_start.py

CMD python3 /bot_start.py;
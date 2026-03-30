FROM python:3 

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache


WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY google_api ./google_api
COPY utils ./utils
COPY models ./models
# COPY res ./res
COPY main.py ./

ENTRYPOINT [ "poetry", "run", "python", "main.py" ]
# docker build cjwrites/finance_sync
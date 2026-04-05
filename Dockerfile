FROM python:3 

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache


WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

COPY financesync ./financesync

# hacky workaround for python packaging purposes for testing
COPY README.md ./ 

COPY cli.py ./ 

RUN poetry install

ENTRYPOINT [ "poetry", "run", "python", "cli.py", "--sync" ]
# docker build cjwrites/finance_sync
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir setuptools \
    && poetry install --no-root

COPY . .

CMD ["python", "main.py"]
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    openssl \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --no-root

COPY . .

RUN poetry install

RUN mkdir -p ravenspedia/certs && \
    cd ravenspedia/certs && \
    openssl genrsa -out jwt-private.pem 2048 && \
    openssl rsa -in jwt-private.pem -pubout -out jwt-public.pem && \
    openssl req -x509 -newkey rsa:4096 -nodes -days 365 \
        -keyout key.pem -out cert.pem \
        -subj "/C=RU/ST=Moscow-State/L=Moscow/O=HSE/OU=CourseProject/CN=90.156.158.26" && \
    chmod 600 *.pem

# Для отладки - временный CMD
CMD ["tail", "-f", "/dev/null"]
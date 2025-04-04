FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl openssl && \
    rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://install.python-poetry.org | python3 - \
 && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-root

COPY . .

RUN poetry install

# Создание сертификатов (оптимизированная версия)
RUN mkdir -p ravenspedia/certs && \
    cd ravenspedia/certs && \
    openssl genrsa -out jwt-private.pem 2048 && \
    openssl rsa -in jwt-private.pem -pubout -out jwt-public.pem && \
    openssl req -x509 -newkey rsa:4096 -nodes -days 365 \
        -keyout key.pem -out cert.pem \
        -subj "/C=RU/ST=Moscow-State/L=Moscow/O=HSE/OU=CourseProject/CN=90.156.158.26" && \
    chmod 600 *.pem && \
    echo "=== Проверка сертификатов ===" && \
    ls -la && \
    openssl x509 -in cert.pem -text -noout && \
    openssl rsa -in key.pem -check -noout && \
    cd /app

RUN echo '#!/bin/sh\n\
poetry run python ravenspedia/main.py\n\
' > /start.sh && chmod +x /start.sh

# Запуск приложения
CMD ["/start.sh"]
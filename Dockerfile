FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl openssl

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://install.python-poetry.org | python3 - \
 && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-root

COPY . .

RUN poetry install

RUN mkdir -p ravenspedia/certs && \
    cd ravenspedia/certs && \
    openssl genrsa -out jwt-private.pem 2048 && \
    openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem && \
    openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 && \
    chmod 600 *.pem && \
    cd .. && cd ..

# Запуск приложения
CMD ["poetry", "run", "python", "ravenspedia/main.py"]
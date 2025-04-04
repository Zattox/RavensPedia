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

RUN echo '#!/bin/bash\n\
mkdir -p ravenspedia/certs && \n\
cd ravenspedia/certs && \n\
openssl genrsa -out jwt-private.pem 2048 && \n\
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem && \n\
openssl req -new -x509 -key jwt-private.pem -out cert.pem -days 365 -subj "/CN=localhost" && \n\
openssl genrsa -out key.pem 2048 && \n\
chmod 600 *.pem && \n\
cd /app && \n\
poetry run python ravenspedia/main.py\n\
' > /app/start.sh && \
chmod +x /app/start.sh

CMD ["/bin/bash", "/app/start.sh"]
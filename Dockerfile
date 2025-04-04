FROM python:3.12-slim
 
RUN apt-get update && apt-get install -y curl

ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 - \
 && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

COPY poetry.lock pyproject.toml README.md ./

RUN poetry install

COPY . .

CMD ["poetry", "run", "python", "./ravenspedia/main.py"]
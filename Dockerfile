FROM python:3.7.3 as builder
RUN pip install --upgrade pip
RUN apt-get update && apt-get -y install gcc
RUN pip install poetry
WORKDIR /gbfs

COPY . .
COPY pyproject.toml poetry.lock /gbfs/
RUN poetry install
RUN poetry build
RUN poetry export -f requirements.txt -o  requirements.txt

FROM builder

RUN pip install -r requirements.txt
RUN pip install dist/*.whl

CMD ["uwsgi", "--http", "0.0.0.0:5000", "--module", "gbfs.wsgi:app"]



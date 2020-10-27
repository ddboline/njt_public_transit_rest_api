FROM python:3.8.6-slim

RUN apt-get update \
  && apt-get -y install wget unzip postgresql-client-common postgresql-client-11 \
  && apt-get clean

RUN mkdir -p /rest_api
WORKDIR /rest_api

COPY requirements.txt /rest_api/requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /rest_api
COPY ./run_tests.sh /rest_api
COPY ./scripts/import_data.sh /rest_api/import_data.sh
COPY ./sql/ /rest_api/sql/
COPY ./data/ /rest_api/data/

COPY . /rest_api

CMD ["./entrypoint.sh"]


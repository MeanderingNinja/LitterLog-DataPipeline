FROM python:3.10

RUN mkdir -p /opt/cat_data_schema/ingest

COPY MANIFEST.in /cat_data_schema/ingest/.
COPY README.md /opt/cat_data_schema/ingest/.
COPY VERSION /opt/cat_data_schema/ingest/.
COPY CatDataSchema /opt/cat_data_schema/ingest/CatDataSchema
COPY setup.py /opt/cat_data_schema/ingest/.
COPY requirements.txt /opt/cat_data_schema/ingest/.
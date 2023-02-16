FROM python:3.10
# Added on 20230216 to solve the "Failed to clean the workspace" error
USER cat_dev_jenkins

RUN mkdir -p /opt/catwatcher/cat_data_schema/ingest

COPY MANIFEST.in opt/catwatcher/cat_data_schema/ingest/. 
COPY README.md /opt/catwatcher/cat_data_schema/ingest/.
COPY VERSION /opt/catwatcher/cat_data_schema/ingest/.
COPY CatDataSchema /opt/catwatcher/cat_data_schema/ingest/CatDataSchema
COPY setup.py /opt/catwatcher/cat_data_schema/ingest/.
COPY requirements.txt /opt/catwatcher/cat_data_schema/ingest/.
COPY test /opt/catwatcher/cat_data_schema/ingest/test

RUN pip install -e /opt/catwatcher/cat_data_schema/ingest
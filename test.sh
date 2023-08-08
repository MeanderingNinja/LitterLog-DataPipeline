#!/bin/bash -e

if [ ! -d .testenv ]; then
    python3 -m venv .testenv
fi

source ".testenv/bin/activate"
pip install -r requirements.txt
pip install -r test_requirements.txt
pip install -e .
pip install pytest pytest-mock requests-mock

# Test DBs Start
echo "Starting TestData DB ..."
sudo docker stop testdata_test_db || true

sudo docker run -d --rm -e "POSTGRES_USER=testdata" -e "POSTGRES_PASSWORD=testdata" -e "POSTGRES_DB=testdata" --name testdata_test_db -p 28431:5432 postgres
export TESTDATA_DATABASE_URL="postgresql://testdata:testdata@localhost:28431/testdata"

sleep 3 # Wait for docker

ARGS=${*:-test}
echo "Running Unit Tests ..."
pytest $ARGS

# Test DB Stop
echo "Stopping Test DBs ..."
sudo docker stop testdata_test_db || true

# Formatting test
echo "Testing formatting..."
black --check CatDataSchema
#black CatDataSchema
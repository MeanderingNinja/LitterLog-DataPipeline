# Cat Data Schema

Repository containing the cat data schema for data storage and visualization using sqlalchemy, alembic, and postgresql

## building

You can build the kernel.test.schema docker by running build.sh
    ./build.sh
this will build a container with tag `test_station_watcher:latest`

to interact with the container, use
    docker run -it --name watcher test_station_watcher:latest /bin/bash

### Notes (running on WSL:Ubuntu)

From the kernel.test.schema directory

    pip install -e .

Installing postgresql (needs to be done before installing pyscopg2)

    sudo apt install postgresql postgresql-contrib
    sudo service postgresql start
    sudo service postgresql status
    sudo apt install libpq-dev

Install pyscopg2

    pip install psycopg2

Generating new migrations
./alembic.sh revision --autogenerate -m "myfirstmigration"

## Deploying to Production

### Prod environment

We deploy onto our on-site `util` server using the docker/docker-compose.yml via a service at `/etc/systemd/system/test_station.service`.

Only the test_station_watcher service depends on kernel.test.schema, the other services are pulled from external registries.

### Deploy updated kernel.test.schema

Deploying is manual right now, you should clone this repo onto util to build the watcher container:

    ```bash
    cd path/to/test-station-schema/kernel.test.schema
    docker build . -t registry.kernel.corp/software/test_station_watcher:latest -f docker/Dockerfile
    docker login registry.kernel.corp
    docker image push registry.kernel.corp/software/test_station_watcher:latest
    ```

Then restart the watcher service

    ```bash
    systemctl restart test_station.service
    ```

### Migrate db in prod

After deploying the latest container, if you need to run alembic migrations:

    ```bash
    docker exec -it test_station_watcher_1 /bin/bash
    # inside bash
    kts-migrate
    ```

# Running the Docker Container (Written on 20221108, not tested after writing)

## Cloning the Repo
To download the code, navigate to a folder of your choosing on your machine
```
git clone https://github.com/emma-jinger/cat_data.git 
```
## Build the Docker Image
Build our docker image `cat_data_watcher:latest` by running: 
```
./build.sh
```
## Spin up the containers (metabase, postgres, nginx, and cat_data_watcher)
Before using docker compose to spin the containers up, modify `DATABASE_URL` in `CatDataSchema/config.py` and `sqlalchemy.url` in `CatDataSchema/alembic.ini` to match the `DATABASE_URL` in `prod-docker-compose.yml`: 
```postgresql+psycopg2://metabase_catwatcher_user:metabase_catwatcher_pw@db:5432/metabase_catwatcher_db```

Spin up the container with the commands: 
```
cd docker 
sudo docker compose up -f prod-docker-compose.yml
```
## Check the data on Metabase 
Go to the browser using `http://192.168.1.157:3001`, you should be able to see cat data whenever there is a new file generated. 


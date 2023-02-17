# Cat Data Schema

Repository containing the cat data schema for data storage and visualization using sqlalchemy, alembic, and postgresql
# What does this program do?
It watches new csv files in `/var/nfs/cat_watcher_output` (produced by the CatWatcher program running in the Nano device and mounted to this directory).
When a new file is found, it loads the data to the database `metabase_catwatcher_db`, which is defined in `config.py`.
This program is setup to be a service running in the background, so it is always running on the server (`cat_tech_server`).
![cat data etl diagram](https://github.com/emma-jinger/cat_data/blob/main/cat_data_etl_diagram.png)
# The File Structure of this Project
This is made into a Python package, which can be installed by using the command `pip install -e .`
```
Working directory: /home/cat_dev/cat_tech/cat_data_pipeline_venv/
.
└── cat_data/
    ├── CatDataSchema/
    │   ├── __init__.py
    │   ├── alembic/
    │   │   ├── env.py
    │   │   ├── README
    │   │   ├── script.py.mako
    │   │   └── versions/
    │   │       └── 9722539bc713_initiate_model_20220823.py
    │   ├── alembic.ini
    │   ├── cli.py
    │   ├── config.py
    │   ├── models.py
    │   └── simple_etl.py
    ├── MANIFEST.in
    ├── README.md
    ├── requirements.txt
    ├── setup.py
    ├── VERSION
    └── .gitignore
```


# Building the Project from Source (Written on 20221108, tested to work in my existing virtual env dir).
**Before building, make sure:** 
- [The metabase service is set up](https://github.com/emma-jinger/Set-Up-a-Service-on-Ubuntu). The metabase unit file at `/etc/systemd/system/metabase.service` and the service env var file at `/etc/default/metabase` defines its setup. 
- The postgres database is set up with the target role, db, and pw.

## Set up a virtual env in the server (optional)
Create a virtual environment `cat_data_pipeline_venv`
## Cloning the Repo   
To download the code, navigate to your working directory
```
git clone https://github.com/emma-jinger/cat_data.git 
```

## Verify Database Info
- `DATABASE_URL` in `config.py` should match database information in the Metabase service env var file `/etc/default/matabase`.
- Value of `sqlalchemy.url` in `CatDataSchema/alembic` should match the above `DATABASE_URL`.
 
## Build the Data Pipeline from the Project Root (cat_data)
```
pip install -e . 
```
## Check data from metabase 
Go to the address `http://192.168.1.157:3000`

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
## Check the data on Metabase. 
Go to the browser using `http://192.168.1.157:3001`, you should be able to see cat data whenever there is a new file generated. 

# To Do List to modify this documentation/project 20230212
- The package I made does not have a `__init__.py` file in the source directory CatDataSchema. Fix that. And understand why it hasn't affected me yet. 
- Test the package locally and using Docker again to make sure it runs smoothly. 
- Write an article on how I did Unit test on this python package
# Additional feature to add 
- Make a PYPI server and push my package to the server (Write a guide as well)

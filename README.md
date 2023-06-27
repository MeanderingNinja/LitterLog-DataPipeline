# Cat Data Schema
Repository containing an ETL pipeline and a data model for data storage using sqlalchemy, alembic, and postgresql.

# What does this program do?
It watches new csv files in the designated directory `/var/nfs/cat_watcher_output`. When a new file is detected, it loads the data to the database `metabase_catwatcher_db`, which is defined in `config.py`. <br>

This program is setup to be a service running in the background, so it is always running on the server (`cat_tech_server`). <br>
**Please update the following diagram.**
![LitterLog-DataPipeline_Diagram](https://github.com/emma-jinger/LitterLog-DataPipeline/blob/main/Diagrams/LitterLog-DataPipeline_Diagram.png)

# The File Structure of this Project
This is made into a Python package, which can be installed by using the command `pip install -e .`
**Please update the following file structure.**
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
    │   │       └── 2bec3474792c_create_the_cat_data_table_20230223.py
    │   ├── alembic.ini
    │   ├── cli.py
    │   ├── config.py
    │   ├── models.py
    │   └── etl.py
    ├── MANIFEST.in
    ├── README.md
    ├── requirements.txt
    ├── setup.py
    ├── VERSION
    └── .gitignore
```


# Building the Project from Source
## Before building, make sure:
- The postgres database is set up with the target role, database, and password (should match `DATABASE_URL` in `.env`).
- (Optional) [The metabase service](https://github.com/emma-jinger/Set-Up-a-Service-on-Ubuntu) has been configured, with the metabase unit file located at `/etc/systemd/system/metabase.service` and the service environment variable file at `/etc/default/metabase`, defining its setup. This configuration allows for effortless data viewing.  

## Set up a virtual environment on the server (optional)
Create a virtual environment `cat_data_pipeline_venv` using the command `python3 -m venv cat_data_pipeline_venv`

## Cloning the Repo   
To download the code, navigate to your working directory
```
git clone https://github.com/emma-jinger/LitterLog-DataPipeline
```

## Verify Database Info  
- Edit `sqlalchemy.url` in `CatDataSchema/alembic.ini` to match the `DATABASE_URL` defined in the `.env` under the directory `CatDataSchema`.
- Database information in the Metabase service file `/etc/default/matabase` should also match the `DATABASE_URL` defined in the `.env`.
 
## Install the `CatDataSchema` Package from the Project Root (cat_data)
```
pip install -e . 
```
*Refer to [Make-a-Python-Package](https://github.com/emma-jinger/Make-a-Python-Package) to read more about working with Python packages.*

## Run the application `cat_data_watcher` to test the ETL pipeline
```
cat_data_watcher
``` 
*Note: cat_data_watcher can be [set up as a service](https://github.com/emma-jinger/Set-Up-a-Service-on-Ubuntu) so that this app will always be running in the background.*

## Check data from Metabase or the database
Go to the address `http://192.168.1.157:3000` to access the Metabase interface to see the data if Metabase is set up.


You can also check to see the data from the actual database with the following commands:
```bash
psql -U your_postgres_user your_postgres_db -h 127.0.0.1 -W # type in the password when prompted
```
Once you are in the database, see all the schema and tables with this psql command: 
```psql
\dt *.*
```

# Running the Docker Container (Written on 20221108, not tested after writing)
Below is the diagram that explains the docker compose set up.
![catdat_docker_diagram](https://github.com/emma-jinger/cat_data/blob/main/Diagrams/catdata_docker_diagram.png)

## Build the Docker Image
Build our docker image `cat_data_watcher:latest` by running: 
```
sudo ./build.sh
```
Check if the `cat_data_watcher:latest` has been built by running:
```
sudo docker images
```
## Spin up the containers (metabase, postgres, nginx, and cat_data_watcher)
Before using docker compose to spin the containers up, modify `DATABASE_URL` in `CatDataSchema/config.py` and `sqlalchemy.url` in `CatDataSchema/alembic.ini` to match the `DATABASE_URL` in `prod-docker-compose.yml`: 
```postgresql+psycopg2://metabase_catwatcher_user:metabase_catwatcher_pw@db:5432/metabase_catwatcher_db```

Spin up the container with the commands: 
```
cd docker 
sudo docker compose -f prod-docker-compose.yml up
```
*Note: The -f option allows you to specify the name and location of the Compose file to use for starting the Docker containers.*
## Check the data on Metabase. 
Go to the browser using `http://192.168.1.157:3001`, you should be able to see cat data whenever there is a new file generated. 


# Additional feature to add 
- Make a PYPI server and push my package to the server (Write a guide as well)

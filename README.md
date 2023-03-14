# Cat Data Schema

Repository containing the cat data schema for data storage and visualization using sqlalchemy, alembic, and postgresql
# What does this program do?
It watches new csv files in `/var/nfs/cat_watcher_output` (produced by the CatWatcher program running in the Nano device and mounted to this directory).
When a new file is found, it loads the data to the database `metabase_catwatcher_db`, which is defined in `config.py`.
This program is setup to be a service running in the background, so it is always running on the server (`cat_tech_server`).
![cat data etl diagram](https://github.com/emma-jinger/cat_data/blob/main/Diagrams/cat_data_etl_diagram.png)
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


# Building the Project from Source (Tested to work 20230228).
## Before building, make sure:
- [The metabase service is set up](https://github.com/emma-jinger/Set-Up-a-Service-on-Ubuntu). The metabase unit file at `/etc/systemd/system/metabase.service` and the service env var file at `/etc/default/metabase` defines its setup. 
- The postgres database is set up with the target role, db, and pw.

## Set up a virtual env in the server (optional)
Create a virtual environment `cat_data_pipeline_venv` using the command `python3 -m venv cat_data_pipeline_venv`

*Note:* 
*When you install your application using `pip` without a virtual environment, the application is installed globally, which means that it is available to all users and processes on your system. When you run the application, you can access it from any directory by typing the name of the application.* 

*When you install your application using `pip` within a virtual environment, the application is installed only within that virtual environment, and it is not available to other users or processes on the system. To run the application, you need to activate the virtual environment first, and then you can access the application from the activated environment.*

## Cloning the Repo   
To download the code, navigate to your working directory
```
git clone https://github.com/emma-jinger/LitterLog-DataPipeline
```

## Verify Database Info
- `DATABASE_URL` in `config.py` should match the target database that was previously set up.  
- Database information in the Metabase service env var file `/etc/default/matabase` should also match the target database that was previously set up.
- Value of `sqlalchemy.url` in `CatDataSchema/alembic.ini` should match the above `DATABASE_URL`.
 
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

## Check data from metabase or the database
Go to the address `http://192.168.1.157:3000` to access the metabase interface and the data inside.


You can also check to see the data from the actual database with the following commands:
```bash
psql -U metabase_catwatcher_user metabase_catwatcher_db -h 127.0.0.1 -W # type in the password when prompted
```
Once you are in the database, see all the schema and tables with this psql command: 
```psql
\dt *.*
```

# Running the Docker Container (Written on 20221108, not tested after writing)
Below is the diagram that explains the docker compose set up.
![catdat_docker_diagram](https://github.com/emma-jinger/cat_data/blob/main/Diagrams/catdata_docker_diagram.png)

## Cloning the Repo
To download the code, navigate to a folder of your choosing on your machine
```
git clone https://github.com/emma-jinger/cat_data.git 
```
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

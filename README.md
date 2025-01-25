# Service Async API

### Project description

An asynchronous API for the online movie service implemented whit FastAPI.
This service is the entry point for all customers and displays information for home, movies, actors and genres pages, and search functionalities. In the first stage, the service allow only anonymous users. Authorization and authentication functions are not implemented yet.


Technologies used:   
- The application code is written in Python + FastAPI. 
- The application runs under the control of the ASGI server (uvicorn). 
- ElasticSearch is used as storage. 
- Redis is used to cache the data. 
- All system components are run via Docker.   
  
Main entities:
- Film — title, content, creation date, directors, actors, screenwriters, genres, and a link to the file. 
- Actor — first name, last name, films with his participation. 
- Director — first name, last name, films that he directed. 
- Screenwriter — first name, last name, films based on his scripts. 
- Genre — description.

<br>

### Two ways to launch the project:

- *Launch the API with the DB services by running the `docker-compose.yml` from root directory*

- *Launch the functional tests from the directory `async_api/tests/functional/`* 

<br>

*All environment variables samples are included in the `.env.sample` files.*

*Don't forget to set the environment variables before running the project!*


<br>

### Technologies used:

![Technologies used](https://skillicons.dev/icons?i=python,fastapi,nginx,redis,elasticsearch,docker)

###### Python, Fastapi, Nginx, Redis, Elasticsearch, Docker

<br><br>

###### (*) *Do not use this project for a real deployment*.

<br>

# Run the project

### 1. Set the environment variables 

```
Change all .env.sample files to .env and set the environment variables in the next locations:

- async_api/etl_loader/env/prod/.env
- async_api/fastapi/env/prod/.env
- async_api/.env
```

### 2. Run docker-compose.yml

```
$ cd async_api/

$ sudo docker compose up 
```

<br><br>

# Run Functional Tests

### 1. Set the environment variables 

```
Change the .env.sample file to .env and set the environment variables in the next location:

- async_api/tests/functional/.env
```

### 2. Run tests, database, and API service.

```
$ cd async_api/tests/functional/

$ sudo docker compose -f docker-compose.db.yaml \
   -f docker-compose.api.yaml \
   -f docker-compose.tests.yaml \
   up -d --build
```

<br>

### Project structure
----

<br>

```

async_api
    ├── etl_loader
    │   ├── docs
    │   ├── env/prod
    |   │   └── .env.example
    │   ├── indices
    │   ├── process
    |   │   └── elasticloader.py
    │   ├── utils
    |   │   └── logger.py
    │   ├── Dockerfile
    │   ├── load_data.py
    |   └── requirements.txt
    |
    ├── fastapi
    │   ├── env/prod
    |   │   └── .env.example
    │   ├── src
    │   │   ├── api/v1
    │   │   │   ├── __init__.py
    │   │   │   ├── films.py
    │   │   │   ├── genres.py
    │   │   │   └── persons.py
    │   │   ├── core
    │   │   │   ├── config.py
    │   │   │   └── logger.py
    │   │   ├── db
    │   │   │   ├── elastic.py
    │   │   │   └── redis.py
    │   │   ├── models
    │   │   │   ├── abstract.py
    │   │   │   ├── film.py
    │   │   │   ├── genre.py
    │   │   │   └── person.py
    │   │   ├── services
    │   │   │   ├── film.py
    │   │   │   ├── genre.py
    │   │   │   └── person.py
    │   │   ├── utils
    │   │   │   ├── abstract.py
    │   │   │   ├── enums.py
    │   │   │   ├── es.py
    │   │   │   └── orjson.py
    │   │   ├── app.sh
    │   │   └── main.py
    │   ├── Dockerfile
    |   └── requirements.txt
    |
    ├── nginx
    |   ├── configs
    │   │   └── site.conf
    │   ├── Dockerfile
    │   └── nginx.conf
    |
    ├── tests
    |   ├── __init__.py
    │   └── functional
    |       ├── fixtures
    |       |   ├── es_fixtures.py
    |       |   ├── redis_fixtures.py
    │       │   └── request_fixtures.py
    |       ├── src
    |       |   ├── __init__.py
    |       |   ├── test_film.py
    |       |   ├── test_genre.py
    |       |   ├── test_person.py
    │       │   └── test_search.py
    |       ├── testdata
    |       ├── utils
    |       ├── __init__.py
    |       ├── .env.sample
    |       ├── conftest.py
    |       ├── docker-compose.api.yml
    |       ├── docker-compose.db.yml
    |       ├── docker-compose.tests.yml
    |       ├── Dockerfile
    |       ├── entrypoint.sh
    |       ├── requirements.txt
    |       └── settings.py
    |
    ├── .env.example
    ├── docker-compose.yml
    └── README.md

```

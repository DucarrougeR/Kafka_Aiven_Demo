# Demo Kafka to Aiven's PostgreSQL

## 1. Kafka

Validate the Kafka dir is there:

`$ ./check_kafka.sh`

## 2. Env Variables

For all these [**go to your Aiven account**](https://console.aiven.io/) to retrieve these values.
To run the application you need multiple Env Vars;

- `AIVEN_API_URL` the URI for Aiven's API (Ensure you exclude the trailing `/` from the value for the env var)
- `AIVEN_TOKEN` the token for the Aiven user to make the calls for the PostgreSQL services

To test the application you will also need these Env Vars to test the psql service;

- `TEST_HOST`
- `TEST_PASSWORD` 
- `TEST_DB_NAME` 
- `TEST_PORT`
- `TEST_USER`


### 3. Start the Kafka env

You will need to have your Zookeeper server up. Run these commands in a terminal:

`$ cd kafka_2.13-3.0.0/`

`$ bin/zookeeper-server-start.sh config/zookeeper.properties`

You will also need to have your Kafka server running. Run these commands in a another terminal:

`$ cd kafka_2.13-3.0.0/`

`$ bin/kafka-server-start.sh config/server.properties`


### 4. Test and Run the demo

First ensure all packages/dependencies are installed on your environment.

`$ pip3 install -r requirements.txt`

Test the demo with the following command:

`$ pytest`

Run the demo with the following command:

`$ python3 demo`

_Developped on python version 3.9_


## 5. Design Decisions

Work with Kafka using the kafka-python package for the Kafka Producer & Consumer.
Work with the Aiven API to validate the project & service existed for PostgreSQL database.
Retrieve information about PostgreSQL db URI to use in Kafka Consumer to update records.

In working with the database, the current implementation uses parametrized SQL in PostgreSQL commands, but could also have used an ORM package like [SQLAlchemy](https://www.sqlalchemy.org/).

#### 5.1 Thoughts on future improvements

1. As this package is intended as a demo it focuses on delivering a functional prototype, with some logging, error handling, testing and documentation. 
2. **Testing** of some functionalities is included but has room from growth in coverage.
3. The repo should also be set up with **CICD** (eg: Actions on Github) for better observability throughout the dev phase and for iterations after release.
3. For greater **portability**, we could also leverage Docker to containerize the application and access mutli-cloud deployments easily.
3. In terms of future deployment, for **scaling** this demo app, we could look into more robust threading and making asynchronous calls (eg: asyncio).
3. Regarding **additional features** for the application, specific parts are currently using hard-coded logic for demonstration purposes (Kafka Topic, Kafka messages, Aiven project name...), these would be made dynamic to let user decide on these (via a config file or some UI selection if this is to be used in a web app).


## 6. External Resources:

- [Kafka Python Package Docs](https://kafka-python.readthedocs.io/en/master/)
- [Kafka Python Package code](https://github.com/dpkp/kafka-python/)
- [Public Github Repo](https://github.com/quay/quay/blob/master/data/logs_model/logs_producer/kafka_logs_producer.py)
- [Consumer De-Serializer](https://medium.com/@mukeshkumar_46704/consume-json-messages-from-kafka-using-kafka-pythons-deserializer-859f5d39e02c)
- [Aiven Event based programming](https://aiven.io/blog/introduction-to-event-based-programming)
- [Aiven blog Python & Postgres](https://aiven.io/blog/the-pursuit-of-happiness-with-python-and-postgresql)
- [psycopg2 repo](https://github.com/psycopg/psycopg2)
- [responses package for API test mocks](https://github.com/getsentry/responses)
- [pytest-kafka test package](https://gitlab.com/search?search=partial&group_id=&project_id=7980450&scope=&search_code=true&snippets=false&repository_ref=master&nav_source=navbar)

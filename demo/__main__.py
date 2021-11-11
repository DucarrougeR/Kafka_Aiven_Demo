import os
from time import sleep
import threading
from loguru import logger
from src.r_kafka_producer import DemoKafkaProducer
from src.r_kafka_consumer import DemoKafkaConsumer
from src.r_aiven_service import DemoAivenStorage


def main():

    # Validate our Aiven setup
    try:
        API_URL = os.environ["AIVEN_API_URL"]
        TOKEN = os.environ["AIVEN_TOKEN"]
    except KeyError as ke:
        logger.critical(f"Missing or Incorrect Env Var(s): {ke}")

    aiven_setup = DemoAivenStorage(API_URL, TOKEN)
    all_projects = aiven_setup.get_project_names()

    # hardcoded for demo purpose
    # IRL we'd likely allow user input for Project name to use
    if "romainducarrouge-31f2" not in all_projects:
        logger.error("Please ensure the right Project is created or that "
                     + "you are connecting with the right credentials")
    else:
        logger.success("Aiven Project for demo application found.")
        for project in all_projects:
            all_services = aiven_setup.get_services(project)

            # hardcoded for demo
            # IRL we'd likely allow user input for service name/type to use
            if 'pg-216f7124' not in all_services:
                logger.error("Please ensure the Service was created or that "
                             + "your API user has access to it")
            else:
                logger.success("Aiven Service for PSQL found.")
                db_uri_params = aiven_setup.get_db_uri_params('pg-216f7124')

    # Initiate the Kafka Producer and Consumer
    demo_topic = 'aiven-job-demo2'
    test_producer = DemoKafkaProducer(demo_topic)
    test_consumer = DemoKafkaConsumer(demo_topic, db_uri_params)

    threads = [
        test_consumer,
        test_producer,
    ]

    for t in threads:
        t.start()
        logger.trace(f"Started thread for: {t}")

    sleep(20)
    logger.success("Demo application complete.")


if __name__ == "__main__":
    main()

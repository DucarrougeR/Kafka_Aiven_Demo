import threading
import json

from typing import Dict, List
from loguru import logger
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from src.r_db_storage import postgresDB


class DemoKafkaConsumer(threading.Thread):
    """Implement the Kafka Consumer.

    Subscribe to the user defined Kafka topic.
    Capture the produced messages.
    Send the event to the destination database.

    Attributes:
      topic: The Kafka Topic to consume.
      db_uri_params: The URI parameters for the DB to store messages.
    """

    daemon = True
    bootstrap_servers = 'localhost:9092'
    timeout = 3000

    def __init__(self,
                 topic: str,
                 db_uri_params: Dict[str, str]
                 ) -> None:
        self.topic = topic
        self.db_uri_params = db_uri_params
        threading.Thread.__init__(self)
        logger.info(f"New DemoKafkaConsumer object generated.")

    def __repr__(self) -> str:
        return f"Consumer(bootstrap_servers = {DemoKafkaConsumer.bootstrap_servers})"

    def run(self) -> List[object]:
        """Generate a Kafka Consumer.
        Subscribe to the predefined topic.
        Consume and send the messages to the datastore.
        """
        try:
            consumer = KafkaConsumer(
                bootstrap_servers=DemoKafkaConsumer.bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
        except Exception as e:
            logger.error(e)

        try:
            consumer.subscribe(self.topic)
            logger.info(f"DemoKafkaConsumer subscribed to topic {self.topic}.")
        except NoBrokersAvailable as nba:
            logger.exception(f"Consumer ran into error subscribing to topic "
                             + f"{self.topic}. Exception: {nba}.")
            logger.exception(f"Ensure Kafka is running and “bootstrap_servers” "
                             + "detail are correct")
        except Exception as e:
            logger.exception(f"Unable to assign topic {self.topic} "
                             + "to DemoKafkaConsumer")

        for message in consumer:
            logger.info(f"Consumer captured: {message.value}")

            # instatiate our datastore object to update the db entries
            database = postgresDB(self.db_uri_params)
            database.write_data(
                message.value["item"],
                message.value["log_time"],
                message.value["error"]
            )

        return [msg.value for msg in consumer]

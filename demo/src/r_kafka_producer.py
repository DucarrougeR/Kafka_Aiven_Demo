import threading
import json
import random
from time import sleep
from datetime import datetime
from loguru import logger

from kafka.errors import KafkaError, KafkaTimeoutError
from kafka import KafkaProducer


class DemoKafkaProducer(threading.Thread):
    """Implement the Kafka Producer.

    Create a user defined Kafka topic.
    Produce arbitrary messages.

    Attributes:
      topic: The Kafka Topic to use for Producer.
    """

    daemon = True
    bootstrap_servers = 'localhost:9092'
    timeout = 3000

    def __init__(self, topic: str) -> None:
        threading.Thread.__init__(self)
        self.topic = topic
        logger.info(f"DemoKafkaProducer object generated.")

    def __repr__(self) -> str:
        return (f"Producer(bootstrap_servers="
                + f"{DemoKafkaProducer.bootstrap_servers} topic={self.topic})")

    def run(self) -> None:
        """Generate and sends the messages to the defines Topic."""
        producer = KafkaProducer(
            bootstrap_servers=DemoKafkaProducer.bootstrap_servers,
            retries=2,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        try:
            # arbitrary logic/value for demo purposes
            for item in range(100):
                errorLevel = "warning" if random.random() > 0.5 else "debug"

                producer.send(self.topic, {'item': item,
                                           'log_time': str(datetime.now()),
                                           'error': errorLevel
                                           })
                sleep(0.5)
            logger.info(f"Publishing records for topic: {self.topic} "
                        + "was successful.")

        except KafkaTimeoutError as te:
            logger.exception(f"Producer timeout issue sending log for "
                             + f"topic: {self.topic}. Exception: {te}.")
        except KafkaError as ke:
            logger.exception(f"Producer ran into error sending log for "
                             + f"topic: {self.topic}. Exception: {ke}.")
        except Exception as e:
            logger.exception(f"Issue encountered send log. Exception: {e}")

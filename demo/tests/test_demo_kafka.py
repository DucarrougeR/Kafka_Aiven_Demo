import pytest
import json
from loguru import logger
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError


class TestKafkaDemoConsumer():

    def test_topic_subscription(self):
        """Test the Consumer ability to subscribe to the Topic."""
        consumer = KafkaConsumer('aiven-job-demo2')
        sub = consumer.subscription()
        assert sub is not consumer.subscription()
        assert sub == set(['aiven-job-demo2'])
        sub.add('other-topic')
        assert consumer.subscription() == set(['aiven-job-demo2'])
        assert len(consumer.topics()) > 1


class TestKafkaDemoProducer():
    """Make sure Zookeper and Kafka servers are up before running these tests."""

    topic = 'aiven-job-demo2'

    def test_producer(self):
        """Test the Producer sending messages."""
        producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            retries=2,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        messages = []
        for item in range(5):
            result = producer.send(TestKafkaDemoProducer.topic, {
                'item': item,
                'log_time': '2020-11-10 22:29:13.887516',
                'error': 'info'
            })
            messages.append(result)
        producer.close()
        assert producer._closed == True
        assert len(messages) == 5
        assert messages[0] is not None

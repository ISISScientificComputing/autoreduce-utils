import json
import os
import time
import logging

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

from autoreduce_utils.message.message import Message

TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')  #"/queue/DataReady"
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')


class Publisher:
    """
    A class to publish messages to a Kafka topic
    """

    def __init__(self):
        self.logger = logging.getLogger(__package__)
        self.producer = None

        if self.producer is None:
            try:
                self.producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL)
            except NoBrokersAvailable as err:
                self.logger.error("Unable to find a broker: %s".format(err))
                time.sleep(1)

    def push(self, message):
        self.logger.debug("Publishing: %s".format(message))
        try:
            if self.producer:
                if isinstance(message, Message):
                    message_json_dump = message.serialize()
                else:
                    message_json_dump = message
                ack = self.producer.send(TRANSACTIONS_TOPIC, message_json_dump)
                metadata = ack.get()
        except AttributeError:
            self.logger.error("Unable to send %s. The producer does not exist.".format(message))

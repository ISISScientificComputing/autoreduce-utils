import json
import os
import threading
import time
import logging
import traceback

from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from autoreduce_utils.clients.connection_exception import ConnectionException

from autoreduce_utils.message.message import Message

TRANSACTIONS_TOPIC = os.environ.get('KAFKA_TOPIC')  #"data_ready"
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')


class Publisher(threading.Thread):
    """
    A class to publish messages to a Kafka topic
    """

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__package__)
        self.logger.debug("Initializing the producer")
        self.producer = None
        self._stop_event = threading.Event()

        while self.producer is None:
            try:
                self.logger.debug("Getting the kafka producer")
                self.producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
                                              value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            except NoBrokersAvailable as err:
                self.logger.error("Unable to find a broker: %s", (err))
                time.sleep(1)

    def run(self):
        """
        Run the thread
        """
        self.logger.debug("Running the thread")
        while not self._stop_event.is_set():
            time.sleep(1)
            if self._stop_event.is_set():
                break
        self.producer.close()

    def send(self, message):
        """ Publish a message to the topic """
        self.logger.debug("Publishing: %s", (message))
        try:
            if self.producer:
                if isinstance(message, Message):
                    message_json_dump = message.serialize()
                else:
                    message_json_dump = message
                self.producer.send(TRANSACTIONS_TOPIC, message_json_dump)
        except AttributeError:
            self.logger.error("Unable to send %s. The producer does not exist.", (message))


def setup_connection() -> Publisher:
    """
    Starts the Kafka producer.
    """

    publisher = Publisher()

    t1 = threading.Thread(target=publisher.run)
    t1.start()

    return publisher


def main():
    """Entry point for the module."""
    logger = logging.getLogger(__package__)
    try:
        setup_connection()
    except ConnectionException as exp:
        logger.error("Exception occurred while connecting: %s %s\n\n%s",
                     type(exp).__name__, exp, traceback.format_exc())
        raise

    logger.info("Kafka producer started.")


if __name__ == '__main__':
    main()

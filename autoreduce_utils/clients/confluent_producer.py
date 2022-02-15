import os
import threading
import time
import logging
import traceback
from confluent_kafka import Producer, KafkaException
from confluent_kafka import Producer, KafkaException
from autoreduce_utils.clients.connection_exception import ConnectionException

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
        self.delivered_msgs = 0

        config = {'bootstrap.servers': KAFKA_BROKER_URL}

        while self.producer is None:
            try:
                self.logger.debug("Getting the kafka producer")
                self.producer = Producer(config)
            except KafkaException as err:
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

    def stop(self):
        """ Stop the consumer """
        self._stop_event.set()

    def stopped(self):
        """ Return whether the consumer has been stopped """
        return self._stop_event.is_set()

    def send(self, message):
        """ Publish a message to the topic """
        self.logger.debug("Publishing: %s", (message))
        try:
            record_value = message.json()
            self.producer.produce(topic=TRANSACTIONS_TOPIC,
                                  value=bytes(str(record_value), 'utf-8'),
                                  on_delivery=self.on_delivery)
        except AttributeError:
            self.logger.error("Unable to send %s. The producer does not exist.", (message))

    def on_delivery(self, error, message):
        """
        Callback called when a message is successfully delivered
        """
        self.delivered_msgs += 1
        self.logger.info("Delivered Message %s", self.delivered_msgs)
        self.logger.debug("Error: %s. Topic: %s., Message: %s.", error, message.topic(), message.value())


def setup_connection() -> Publisher:
    """
    Starts the Kafka producer.
    """

    publisher = Publisher()

    producer_thread = threading.Thread(target=publisher.run)
    producer_thread.start()

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

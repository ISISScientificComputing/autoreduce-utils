import logging
import os

import confluent_kafka

log = logging.getLogger(__name__)


class Publisher(object):
    """Wrapper around asynchronous Kafka Producer"""

    def __init__(self, **config):
        """
        Create new Producer wrapper instance.

        :param str bootstrap_servers: Initial list of brokers as a CSV
        list of broker host or host:port.
        :param config Configuration properties
        """

        config['bootstrap.servers'] = os.environ.get('KAFKA_BROKER_URL')
        self._producer = confluent_kafka.Producer(config)

    @staticmethod
    def delivery_report(err, msg):
        """
        Callback called once for each produced message to indicate the final
        delivery result. Triggered by poll() or flush().

        :param confluent_kafka.KafkaError err: Information about any error
        that occurred whilst producing the message.
        :param confluent_kafka.Message msg: Information about the message
        produced.
        :returns: None
        :raises confluent_kafka.KafkaException
        """

        if err is not None:
            log.exception('Message delivery failed: %s', (err))
            raise confluent_kafka.KafkaException(err)
        else:
            log.debug('Message delivered to %s [%s]: %s', (msg.topic(), msg.partition(), msg.value()))

    def publish(self, topic, messages, key=None, timeout=2):
        """
        Publish messages to the topic.

        :param str topic: Topic to produce messages to.
        :param list(str) messages:  List of message payloads.
        :param str key: Message key.
        :param float timeout: Maximum time to block in seconds.
        :returns: Number of messages still in queue.
        :rtype int
        """

        if not isinstance(messages, list):
            messages = [messages]

        try:
            for m in messages:
                record_value = m.json()
                self._producer.produce(topic, record_value, key, callback=Publisher.delivery_report)
                self._producer.poll(0)

            return self._producer.flush(timeout)

        except (BufferError, confluent_kafka.KafkaException, NotImplementedError):
            log.exception('Error publishing to %s topic.', (topic))
            raise

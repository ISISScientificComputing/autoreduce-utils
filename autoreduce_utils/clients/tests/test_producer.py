from unittest import TestCase

from autoreduce_utils.clients.producer import Publisher


class TestProducer(TestCase):
    """
    Test Kafka Consumer
    """

    def setUp(self):
        self.producer = Publisher()

    def test_publish(self):
        """
        Test: A message is published to the topic
        When: publish is called
        """
        # Create test json message
        message = {'test': 'test'}
        pass

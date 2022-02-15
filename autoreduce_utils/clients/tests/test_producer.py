# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from unittest import TestCase, mock
import confluent_kafka
from autoreduce_utils.clients import producer
from autoreduce_utils.message.message import Message

FAKE_KAFKA_TOPIC = 'topic'
FAKE_KAFKA_URL = 'FAKE_KAFKA_URL'


class TestConfluentKafkaProducer(TestCase):

    @mock.patch('confluent_kafka.Producer')
    @mock.patch.dict(os.environ, {"KAFKA_BROKER_URL": "FAKE_KAFKA_URL"}, clear=True)
    def setUp(self, mock_confluent_producer):
        """ Set up the test case. """
        super().setUp()
        self.mock_confluent_producer = mock_confluent_producer
        self.prod = producer.Publisher()

    def tearDown(self):
        """ Tear down the test case. """
        super().tearDown()

    def test_kafka_producer_init(self):
        """ Test if the producer is initialized correctly. """
        expected_config = {'bootstrap.servers': FAKE_KAFKA_URL}

        self.mock_confluent_producer.assert_called_once_with(expected_config)
        self.assertEqual(self.mock_confluent_producer.return_value, self.prod._producer)

    def test_kafka_producer_publish(self):
        """ Test if the producer publishes correctly. """
        topic = FAKE_KAFKA_TOPIC
        test_message = Message()
        messages = [test_message]
        expected_message = test_message.json()

        self.prod.publish(topic, messages)

        produce_callback = producer.Publisher.delivery_report
        self.prod._producer.produce.assert_called_once_with(topic, expected_message, None, callback=produce_callback)
        self.prod._producer.flush.assert_called_once()

    def test_kafka_producer_publish_one_message_with_key(self):
        """ Test if the producer publishes correctly with a key. """
        topic = FAKE_KAFKA_TOPIC
        one_message = Message()
        key = '1000'
        expected_message = one_message.json()

        self.prod.publish(topic, one_message, key)

        produce_callback = producer.Publisher.delivery_report
        self.prod._producer.produce.assert_called_once_with(topic, expected_message, key, callback=produce_callback)
        self.prod._producer.flush.assert_called_once()

    def test_kafka_producer_publish_exception(self):
        """ Test if the producer raises an exception when publishing. """
        topic = FAKE_KAFKA_TOPIC
        test_message = Message()
        messages = [test_message]
        self.prod._producer.produce.side_effect = \
            confluent_kafka.KafkaException

        self.assertRaises(confluent_kafka.KafkaException, self.prod.publish, topic, messages)

    @mock.patch('confluent_kafka.Message')
    def test_delivery_report_exception(self):
        """ Test if the delivery report raises an exception when publishing. """
        self.assertRaises(confluent_kafka.KafkaException, self.prod.delivery_report, confluent_kafka.KafkaError,
                          confluent_kafka.Message)

    @mock.patch('confluent_kafka.Message')
    def test_delivery_report(self):
        self.prod.delivery_report(None, confluent_kafka.Message)

    @mock.patch('confluent_kafka.Message')
    def test_delivery_report_with_unicode(self, mock_message):
        """ Test if the delivery report is successful with unicode. """
        mock_message.topic.return_value = 'test_topic'
        mock_message.partition.return_value = '1'
        mock_message.value.return_value = 'gęś'
        self.prod.delivery_report(None, mock_message)

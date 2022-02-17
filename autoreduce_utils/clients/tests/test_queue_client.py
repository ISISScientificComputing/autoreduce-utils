# ############################################################################### #
# Autoreduction Repository : https://github.com/autoreduction/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
Test functionality for the activemq client
"""
import os
import socket

from unittest import TestCase, mock
from unittest.mock import patch, MagicMock

from autoreduce_utils.message.message import Message
from autoreduce_utils.clients.connection_exception import ConnectionException
from autoreduce_utils.clients.queue_client import QueueClient


# pylint:disable=protected-access,no-self-use
class TestQueueClient(TestCase):
    """
    Exercises the queue client
    """

    def test_default_init(self):
        """
        Test: Class variables are created and set
        When: QueueClient is initialised with default credentials
        """

        client = QueueClient()
        self.assertIsNone(client._connection)
        self.assertEqual('queue_client', client._consumer_name)

    def test_valid_connection(self):
        """
        Test: Access is established with a valid connection
        (This by proxy will also test the get_connection function)
        When: connect is called while valid credentials are held
        """

        client = QueueClient()
        client.connect()
        self.assertTrue(client._connection.is_connected())

    @mock.patch.dict(os.environ, {
        "ACTIVEMQ_USERNAME": "not-user",
        "ACTIVEMQ_PASSWORD": "not-pass",
        "ACTIVEMQ_HOST": "127.does.not.exist",
        "ACTIVEMQ_PORT": "1234"
    },
                     clear=True)
    def test_connection_failed_invalid_credentials(self):
        """
        Test: A ConnectionException is raised
        When: _test_connection is called while invalid credentials are held
        """
        client = QueueClient()
        with self.assertRaises(ConnectionException):
            client.connect()

    def test_stop_connection(self):
        """
        Test: Connection is stopped and connection variables are set to None
        When: disconnect is called while a valid connection is currently established
        """

        client = QueueClient()
        mocked_connection = mock.Mock()
        client._connection = mocked_connection

        with mock.patch("uuid.uuid4") as patched_uuid:
            patched_uuid.return_value = 1
            client.disconnect()

        mocked_connection.disconnect.assert_called_with(receipt=str(1))
        self.assertIsNone(client._connection)

    @patch('stomp.connect.StompConnection11.send')
    def test_send_with_raw_string(self, mock_stomp_send):
        """
        Test: send sends the given data using stomp.send
        When: send is called with a string argument for message
        """

        client = QueueClient()
        client.send('dataready', 'raw_json_dump')
        (args, _) = mock_stomp_send.call_args
        self.assertEqual(args[0], 'dataready')
        self.assertEqual(args[1], 'raw_json_dump')

    @patch('stomp.connect.StompConnection11.send')
    def test_send_with_message_instance(self, mock_stomp_send):
        """
        Test: send sends the given data using stomp.send
        When: send is called with a Message instance argument for message
        """

        client = QueueClient()
        message = Message(description="test-message")
        client.send('dataready', message)
        (args, _) = mock_stomp_send.call_args
        self.assertEqual(args[0], 'dataready')
        self.assertEqual(args[1], message.serialize())

    @patch('stomp.connect.StompConnection11.ack')
    def test_ack(self, mock_stomp_ack):
        """
        Test: ack sends an ack frame using stomp.ack
        When: ack is called while a valid connection is held
        """

        client = QueueClient()
        client.connect()
        client.ack("test", "subscription")
        mock_stomp_ack.assert_called_once_with('test', "subscription")

    def test_create_connection_bad_development(self):
        """
        Test: Exception raised
        When: production host used in non production environment
        """

        client = QueueClient()
        real_host = client.activemq_host
        client.activemq_host = "production.domain.com"
        self.assertRaisesRegex(RuntimeError, "non-development", client._create_connection)
        client.activemq_host = real_host

    def test_create_connection_bad_production(self):
        """
        Test: Exception raised
        When: Local host used in production environment
        """

        client = QueueClient()
        real_host = client.activemq_host

        os.environ["AUTOREDUCTION_PRODUCTION"] = "1"
        client.activemq_host = "127.0.0.1"
        self.assertRaisesRegex(RuntimeError, ".*production environment.*", client._create_connection)

        client.activemq_host = "somethingdev"
        self.assertRaisesRegex(RuntimeError, ".*production environment.*", client._create_connection)

        client.activemq_host = "activemq"
        self.assertRaisesRegex(RuntimeError, ".*production environment.*", client._create_connection)

        client.activemq_host = real_host
        del os.environ["AUTOREDUCTION_PRODUCTION"]

    def test_test_connection_not_connected(self):
        """
        Test: Exception raised
        When: test_connection called when not connected
        """

        client = QueueClient()
        mock_connection = MagicMock()
        mock_connection.is_connected.return_value = False
        client._connection = mock_connection
        with self.assertRaises(ConnectionException):
            client._test_connection()

    def test_test_connection_connected(self):
        """
        Test: test_connection returns True
        When: Connected
        """

        client = QueueClient()
        mock_connection = MagicMock()
        mock_connection.is_connected.return_value = True
        client._connection = mock_connection
        self.assertTrue(client._test_connection())

    def test_subscribe(self):
        """
        Test: correct calls made
        When: subscribe is called
        """

        client = QueueClient()
        mock_connection = MagicMock()
        mock_listener = MagicMock()
        client._connection = mock_connection
        client.subscribe(mock_listener)

        mock_connection.set_listener.assert_called_with("queue_processor", mock_listener)
        mock_connection.subscribe.assert_called_with(destination="/queue/DataReady",
                                                     id=socket.getfqdn(),
                                                     ack="client-individual",
                                                     header={"activemq.prefetchSize": "1"})

# ############################################################################### #
# Autoreduction Repository : https://github.com/autoreduction/autoreduce
#
# Copyright &copy; 2020 ISIS Rutherford Appleton Laboratory UKRI
# SPDX - License - Identifier: GPL-3.0-or-later
# ############################################################################### #
"""
Client class for accessing queuing service
"""
import logging
import os
import uuid
import socket

import stomp
from stomp.exception import ConnectFailedException

from autoreduce_utils.message.message import Message
from autoreduce_utils.clients.connection_exception import ConnectionException


class QueueClient():
    """
    Class for client to access messaging service via python
    """

    def __init__(self, consumer_name='queue_client'):
        self.activemq_host = os.getenv("ACTIVEMQ_HOST")
        self.activemq_port = os.getenv("ACTIVEMQ_PORT")
        self.activemq_user = os.getenv("ACTIVEMQ_USERNAME")
        self._connection = None
        self._consumer_name = consumer_name
        self._logger = logging.getLogger(__package__)

    def connect(self):
        """
        Create the connection if the connection has not been created
        """

        if self._connection is None or not self._connection.is_connected():
            self.disconnect()
            self._create_connection()

    def _test_connection(self):
        if self._connection.is_connected():
            return True
        raise ConnectionException("ActiveMQ")

    def disconnect(self):
        """
        Disconnect from queue service
        """

        self._logger.info("Starting disconnect from ActiveMQ...")
        if self._connection is not None and self._connection.is_connected():
            # By passing a receipt Stomp will call stop on the transport layer
            # which causes it to wait on the listener thread (if it's still
            # running). Without this step we just drop out, so the behaviour
            # is not guaranteed. UUID is used by Stomp if we don't pass in
            # a receipt so this matches the behaviour under the hood
            try:
                self._connection.remove_listener("queue_processor")
            except KeyError:
                pass  # If no listener was set for this client instance
            self._connection.disconnect(receipt=str(uuid.uuid4()))
            self._logger.info("Disconnected from ActiveMQ.")
        self._connection = None

    def _create_connection(self):
        """
        Create the connection to the queuing service and store as self._connection
        """

        inteded_for_production = "AUTOREDUCTION_PRODUCTION" in os.environ

        aimed_at_dev = False
        if self.activemq_host.startswith("127") or "dev" in self.activemq_host or "activemq" in self.activemq_host:
            aimed_at_dev = True
        # Prevent unintentional submission to non-development envs
        if not inteded_for_production and not aimed_at_dev:
            raise RuntimeError(
                f"Trying to submit to a potentially non-development environment at `{self.activemq_host}`. "
                "You must declare AUTOREDUCTION_PRODUCTION in the environment "
                "if you intend to submit to the production environment")
        if inteded_for_production and aimed_at_dev:
            raise RuntimeError(f"Trying to submit to production environment but host is `{self.activemq_host}`. "
                               "Remove AUTOREDUCTION_PRODUCTION if that is unintentional.")

        if self._connection is None or not self._connection.is_connected():
            try:
                host_port = [(self.activemq_host, int(self.activemq_port))]
                connection = stomp.Connection(host_and_ports=host_port)
                self._logger.info("Starting connection to %s", host_port)
                connection.connect(username=self.activemq_user, passcode=os.getenv("ACTIVEMQ_PASSWORD"), wait=True)
            except ConnectFailedException as exp:
                raise ConnectionException("ActiveMQ") from exp
            self._connection = connection

    def subscribe(self, listener):
        """
        Subscribes to the data_ready queue
        :param listener: QueueListener object
        """

        self._logger.info("Subscribing to data ready queue")
        self._connection.set_listener("queue_processor", listener)
        self._connection.subscribe(destination='/queue/DataReady',
                                   id=socket.getfqdn(),
                                   ack="client-individual",
                                   header={"activemq.prefetchSize": "1"})

    def ack(self, message_id, subscription):
        """
        Acknowledge receipt of a message
        :param message_id: The identifier of the message
        """
        # pylint:disable=no-value-for-parameter
        self._connection.ack(message_id, subscription)

    def send(self, destination, message, persistent='true', priority='4', delay=None):
        """
        Send a message via the open connection to a queue
        :param destination: Queue to send to
        :param message: Message instance OR json dump of dict containing message payload
        :param persistent: should to message be persistent
        :param priority: priority rating of the message
        :param delay: time to wait before send
        """
        self.connect()

        if isinstance(message, Message):
            message_json_dump = message.serialize()
        else:
            message_json_dump = message

        self._connection.send(destination, message_json_dump, persistent=persistent, priority=priority, delay=delay)

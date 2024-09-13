#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""a_short_module_description"""
# ---------------------------------------------------------------------------

import socket
import logging
import logging.handlers
import threading
import pickle
import struct
import os
import json


logger = logging.getLogger(__name__)


class JsonFormatter(logging.Formatter):
    """Custom JSON formatter for logging that includes extra fields."""

    def format(self, record):
        log_entry = {
            "asctime": self.formatTime(record, self.datefmt),
            "name": record.name,
            "levelname": record.levelname,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            log_entry["stack_info"] = self.formatStack(record.stack_info)
        if record.args:
            log_entry["args"] = record.args
        if hasattr(record, "device"):
            log_entry["device"] = record.device
        return json.dumps(log_entry)


# Define the LogServer class
class LogServer:
    def __init__(self, host="127.0.0.1", port=9000, log_file="logs.txt"):
        self.host = host
        self.port = port
        self.log_file = log_file
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        # Configure FileHandler
        self.file_handler = logging.FileHandler(self.log_file)
        # self.file_handler.setFormatter(
        #     logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # )
        self.file_handler.setFormatter(JsonFormatter())

        # Create and configure logger
        self.aggregated_logger = logging.getLogger("aggregated_logger")
        self.aggregated_logger.setLevel(logging.DEBUG)
        self.aggregated_logger.addHandler(self.file_handler)

    def start(self):
        """Start the server and handle client connections."""
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                logger.info(f"Accepted connection from {client_address}")
                threading.Thread(
                    target=self.handle_client, args=(client_socket,)
                ).start()
        except KeyboardInterrupt:
            logger.info("Shutting down server...")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        """Handle incoming logs from a connected client."""
        with client_socket:
            while True:
                try:
                    # Receive the log record length
                    data = client_socket.recv(4)
                    if not data:
                        break
                    record_length = struct.unpack(">L", data)[0]
                    # Receive the log record itself
                    log_record_data = client_socket.recv(record_length)
                    log_record_dict = pickle.loads(log_record_data)

                    # Recreate a LogRecord object from the dictionary
                    log_record = logging.makeLogRecord(log_record_dict)

                    self.aggregated_logger.handle(
                        log_record
                    )  # Pass the log record to the logger
                    logger.info(f"Received log record: {log_record.getMessage()}")
                except Exception as e:
                    logger.error(f"Error handling client log record: {e}")
                    break
        logger.info("Client disconnected")


# Function to run the server
def run_server():
    log_server = LogServer(host="127.0.0.1", port=9000, log_file="server_logs.txt")
    log_server.start()

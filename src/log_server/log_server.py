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


# Define the LogServer class
class LogServer:
    def __init__(self, host="127.0.0.1", port=9000, log_file="logs.txt"):
        self.host = host
        self.port = port
        self.log_file = log_file
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)  # Allow up to 5 connections

        # Set up local file logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

        print(
            f"LogServer started on {self.host}:{self.port}, writing logs to {self.log_file}"
        )

    def start(self):
        """Start the server and handle client connections."""
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")
                threading.Thread(
                    target=self.handle_client, args=(client_socket,)
                ).start()
        except KeyboardInterrupt:
            print("Shutting down server...")
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

                    # Handle the log record with the logging module
                    logger = logging.getLogger()  # Use the root logger
                    logger.handle(log_record)  # Pass the log record to the logger
                except Exception as e:
                    print(f"Error handling client log record: {e}")
                    break
        print("Client disconnected")


# Function to run the server
def run_server():
    log_server = LogServer(host="127.0.0.1", port=9000, log_file="server_logs.txt")
    log_server.start()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""a_short_module_description"""
# ---------------------------------------------------------------------------


import logging
import logging.handlers
import socket
import threading
import time


def create_log_handler(server_host="127.0.0.1", server_port=9000):
    """Create and return a SocketHandler that connects to the log server."""
    # Set up the SocketHandler to send logs to the server
    socket_handler = logging.handlers.SocketHandler(server_host, server_port)
    return socket_handler


# Define the main function to run both the server and the client
def main():
    # Start the client
    create_log_handler()


if __name__ == "__main__":
    main()

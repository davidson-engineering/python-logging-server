#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""a_short_project_description"""
# ---------------------------------------------------------------------------

import random
import sys
import threading
import time
import logging

from log_server import serve_forever

logger = logging.getLogger()

HOST, PORT = "localhost", 9001


def start_server_thread():

    def run_server():
        serve_forever(HOST, PORT, target="logs.txt")

    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = (
        True  # Daemonize the server thread so it shuts down with the main program
    )
    server_thread.start()

    # Wait a bit to ensure the server has started
    time.sleep(2)


def test_client_logging():

    id = random.randint(1, 1000)

    # Log some messages using the logger
    for i in range(100):
        logger.info(
            f"Log message {i + 1} from application",
            extra={"device": id},
        )
        logger.error("some error", extra={"device": id})
        logger.warning("some warning", extra={"device": id})
        logger.debug("some debug", extra={"device": id})
        time.sleep(0.1)
    logging.shutdown()


def start_client_thread():
    client_thread = threading.Thread(target=test_client_logging)
    client_thread.start()


# Define the main function to create the server and client
def main():
    # Create a logger and add the handler
    remote_logging_handler = logging.handlers.SocketHandler(host=HOST, port=PORT)
    stream_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(
        level=logging.INFO,
        handlers=[remote_logging_handler, stream_handler],
    )
    # start_server_thread()
    test_client_logging()

    for i in range(10):
        start_client_thread()


if __name__ == "__main__":
    main()

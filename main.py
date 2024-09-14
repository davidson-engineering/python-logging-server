#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""a_short_project_description"""
# ---------------------------------------------------------------------------

import threading
import time
import logging

from log_server import serve_forever

logger = logging.getLogger()

HOST, PORT = "127.0.0.1", 9009


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

    # Log some messages using the logger
    for i in range(10000):
        logger.info(
            f"Log message {i + 1} from application",
            extra={"device": "my_unique_device_id"},
        )
        # time.sleep(0.001)


# Define the main function to create the server and client
def main():
    # Create a logger and add the handler
    remote_logging_handler = logging.handlers.SocketHandler(host=HOST, port=PORT)
    stream_handler = logging.StreamHandler()
    logging.basicConfig(
        level=logging.INFO,
        handlers=[remote_logging_handler, stream_handler],
    )
    test_client_logging()


if __name__ == "__main__":
    main()

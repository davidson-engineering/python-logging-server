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
import threading
import time
import logging
import logging.handlers

from log_server import serve_forever

logger = logging.getLogger()

HOST, PORT = "127.0.0.1", 18845


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


def get_device_id():
    return f"device_{random.choice(range(1, 1000)):04d}"


def get_log_messag_type():
    # choose a random log message type
    messages = ["info", "error", "warning", "debug"]
    message = random.choice(messages)
    return message


def create_log(device_id: str = None):

    device_id = device_id or get_device_id()
    log_type = get_log_messag_type()

    # Log some messages using the logger
    if log_type == "info":
        logger.info(
            f"Useful message from application",
            extra={
                "device_id": device_id,
                "custom_data": "some data",
                "host": "localhost",
            },
        )
    elif log_type == "error":
        logger.error(
            "Something went horribly wrong",
            extra={"device_id": device_id, "host": "localhost"},
        )
    elif log_type == "warning":
        logger.warning(
            "something is not right, and you should know about it",
            extra={"device_id": device_id, "host": "localhost"},
        )
    elif log_type == "debug":
        logger.debug(
            "This information might prove useful later",
            extra={
                "device_id": device_id,
                "host": "localhost",
                "useful_debug_output": random.randint(1, 10000),
            },
        )

    pause = random.random() * 10
    time.sleep(pause)


# Define the main function to create the server and client
def main():
    # Create a logger and add the handler
    remote_logging_handler = logging.handlers.SocketHandler(host=HOST, port=PORT)
    stream_handler = logging.StreamHandler()
    logging.basicConfig(
        level=logging.INFO,
        handlers=[remote_logging_handler, stream_handler],
        format="%(asctime)s - %(levelname)s - (%(device_id)s) %(message)s",
    )

    def logging_func():
        device_id = get_device_id()
        while True:
            create_log(device_id)

    for _ in range(250):
        threading.Thread(target=logging_func).start()


if __name__ == "__main__":
    main()

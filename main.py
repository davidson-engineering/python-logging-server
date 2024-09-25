#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2024-09-14
# version ='1.0'
# ---------------------------------------------------------------------------
"""Logging client to send logs to a remote server"""
# ---------------------------------------------------------------------------

from __future__ import annotations


# Server Configuration
# --------------------
# Logging server can  be started by running the following command:
# from log_server import serve_forever
# serve_forever(HOST, PORT, target="logs.txt")
# Note that the server will run indefinitely until it is stopped manually
# and this call will block the current thread.

# Client Configuration
# --------------------
import logging.handlers
from math import factorial
import sys

# The address of the logging server
HOST, PORT = "localhost", 9001

logger = logging.getLogger("remote_logging_app")


def work(i: int) -> int:
    logger.info("Factorial %d", i)
    f = factorial(i)
    logger.info("Factorial(%d) = %d", i, f)
    return f


def main():
    socket_handler = logging.handlers.SocketHandler(HOST, PORT)
    stream_handler = logging.StreamHandler(sys.stderr)
    logging.basicConfig(
        level=logging.INFO,
        handlers=[socket_handler, stream_handler],
    )

    for i in range(10):
        work(i)

    logging.shutdown()


if __name__ == "__main__":
    main()

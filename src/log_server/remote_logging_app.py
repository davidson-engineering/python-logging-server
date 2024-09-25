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
import logging
import logging.handlers
from math import factorial
import sys

logger = logging.getLogger("remote_logging_app")

HOST, PORT = "localhost", 9001


def work(i: int) -> int:
    logger.info("Factorial %d", i)
    f = factorial(i)
    logger.info("Factorial(%d) = %d", i, f)
    return f


# Define the main function to run both the server and the client
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

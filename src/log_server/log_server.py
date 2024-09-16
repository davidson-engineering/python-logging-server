#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2024-09-14
# version ='1.0'
# ---------------------------------------------------------------------------
"""Logging server to receive logs from multiple clients"""
# ---------------------------------------------------------------------------

from __future__ import annotations
import json
from pathlib import Path
import threading
from typing import TextIO
import socketserver
import pickle
import struct
import logging
from datetime import datetime
import prometheus_client

logger = logging.getLogger(__name__)


def format_log(payload):
    # convert created time to human readable format
    dt = datetime.fromtimestamp(payload["created"])
    payload["created_human"] = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


class LogDataCatcher(socketserver.BaseRequestHandler):

    log_file: TextIO
    size_format = ">L"
    size_bytes = struct.calcsize(size_format)
    file_lock = threading.Lock()

    logging_server_log_count = prometheus_client.Counter(
        "logging_server_log_count",
        "Number of logs received by the logging server",
        ["client"],
    )

    def handle(self):
        logger.info(f"Received connection from {self.client_address}")
        # Receive and unpack the message
        size_header_bytes = self.request.recv(LogDataCatcher.size_bytes)
        while size_header_bytes:
            payload_size = struct.unpack(LogDataCatcher.size_format, size_header_bytes)
            payload_bytes = self.recv_all(self.request, payload_size[0])
            payload = pickle.loads(payload_bytes)
            LogDataCatcher.logging_server_log_count.labels(
                client=str(self.client_address)
            ).inc()
            # Apply custom formatting
            format_log(payload)
            with LogDataCatcher.file_lock:
                self.log_file.write(json.dumps(payload) + "\n")
            try:
                size_header_bytes = self.request.recv(LogDataCatcher.size_bytes)
            except (ConnectionResetError, BrokenPipeError):
                logger.warning("Connection closed by client")
                break

    def recv_all(self, sock, size):
        """Helper function to receive the exact number of bytes required."""
        data = b""
        while len(data) < size:
            packet = sock.recv(size - len(data))
            if not packet:
                raise EOFError("Connection closed while receiving data")
            data += packet
        return data


def serve_forever(host, port, target: Path, multithreaded=False):
    # Create a TCP server, bind it to the host and port, and start serving

    # Choose the server factory based on the multithreaded flag
    if multithreaded:
        server_factory = socketserver.ThreadingTCPServer
    else:
        server_factory = socketserver.TCPServer

    # Open the target file for writing
    if isinstance(target, str):
        target = Path(target)

    with target.open("w") as unified_log:
        LogDataCatcher.log_file = unified_log

        try:
            with server_factory((host, port), LogDataCatcher) as server:
                logger.info(f"Starting server on {host}:{port}")

                server.serve_forever()

        except OSError as e:
            logger.error(f"Failed to start server on {host}:{port} {e}")


if __name__ == "__main__":
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format="%(asctime)s - %(message)s",
    #     handlers=[logging.StreamHandler()],
    # )
    serve_forever("localhost", 9001, target="logs.txt", multithreaded=False)

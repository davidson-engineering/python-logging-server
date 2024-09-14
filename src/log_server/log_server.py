from __future__ import annotations
import json
from pathlib import Path
from typing import TextIO
import socketserver
import pickle
import struct
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def format_log(payload):
    # convert created time to human readable format
    dt = datetime.fromtimestamp(payload["created"])
    payload["created_human"] = dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


class LogDataCatcher(socketserver.BaseRequestHandler):

    log_file: TextIO
    count: int = 0
    size_format = ">L"
    size_bytes = struct.calcsize(size_format)

    def handle(self):
        logger.info(f"Received connection from {self.client_address}")
        # Receive and unpack the message
        size_header_bytes = self.request.recv(LogDataCatcher.size_bytes)
        while size_header_bytes:
            payload_size = struct.unpack(LogDataCatcher.size_format, size_header_bytes)
            payload_bytes = self.request.recv(payload_size[0])
            payload = pickle.loads(payload_bytes)
            LogDataCatcher.count += 1
            # Apply custom formatting
            format_log(payload)
            self.log_file.write(json.dumps(payload) + "\n")
            try:
                size_header_bytes = self.request.recv(LogDataCatcher.size_bytes)
            except (ConnectionResetError, BrokenPipeError):
                logger.warning("Connection closed by client")
                break


def serve_forever(host, port, target: Path):
    if isinstance(target, str):
        target = Path(target)
    with target.open("w") as unified_log:
        LogDataCatcher.log_file = unified_log
        try:
            with socketserver.TCPServer((host, port), LogDataCatcher) as server:
                logger.info(f"Starting server on {host}:{port}")
                server.serve_forever()
        except OSError as e:
            logger.error(f"Failed to start server on {host}:{port} {e}")


if __name__ == "__main__":
    serve_forever("localhost", 9001, target="logs.txt")

from __future__ import annotations
import json
from pathlib import Path
from typing import TextIO
import socketserver
import pickle
import struct
import logging

logger = logging.getLogger(__name__)


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
        with socketserver.TCPServer((host, port), LogDataCatcher) as server:
            logger.info(f"Starting server on {host}:{port}")
            server.serve_forever()


if __name__ == "__main__":
    serve_forever()

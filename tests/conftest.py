from __future__ import annotations
import subprocess
import signal
import socket
import sys
import time
import pytest
import logging
import log_server.remote_logging_app as remote_logging_app
from typing import Iterator


@pytest.fixture(scope="session")
def logging_server() -> Iterator[None]:
    print("Starting log server")
    p = subprocess.Popen(
        ["python3", "src/log_server/log_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    time.sleep(0.25)

    yield

    p.terminate()
    p.wait()
    if p.stdout:
        print(p.stdout.read())
    assert (
        p.returncode == -signal.SIGTERM.value
    ), f"Error in watcher, return code={p.returncode}"


@pytest.fixture
def logging_config() -> Iterator[None]:
    HOST, PORT = "localhost", 9001
    socket_handler = logging.handlers.SocketHandler(HOST, PORT)
    # remote_logging_app.logger.addHandler(socket_handler)
    logging.basicConfig(level=logging.INFO, handlers=[socket_handler])

    yield

    socket_handler.close()
    remote_logging_app.logger.removeHandler(socket_handler)

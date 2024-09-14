import socket
import threading
import time
import pytest

from log_server.log_server_old import LogServer

HOST = "127.0.0.1"


@pytest.fixture
def server(tmp_path):
    """Fixture to create a LogServer instance with a temporary log file."""

    def find_available_port():
        """Find and return an available port."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            return s.getsockname()[1]

    port = find_available_port()
    log_file = tmp_path / f"test_logs_{time.time_ns()}.txt"
    server_instance = LogServer(host=HOST, port=port, log_file=str(log_file))
    threading.Thread(target=server_instance.start, daemon=True).start()
    # Give the server some time to start
    time.sleep(1)
    yield server_instance, log_file, HOST, port
    server_instance.server_socket.close()

import time
import logging
from src.log_server import create_log_handler


def test_client_logging(server):
    """Test client logging to a running LogServer instance."""
    server_instance, log_file, host, port = server
    logger = logging.getLogger("ClientTestLogger")
    logger.setLevel(logging.INFO)
    handler = create_log_handler(server_host=host, server_port=port)
    logger.addHandler(handler)

    logger.info("Client test message")

    time.sleep(1)

    with open(log_file, "r") as file:
        logs = file.read()

    assert "Client test message" in logs

import time
import logging
import pickle
import struct
from unittest.mock import MagicMock, patch


@patch("socket.socket")
def test_handle_client(mock_socket, server):
    """Test the handle_client method of LogServer."""
    server_instance, _, _, _ = server
    mock_client_socket = MagicMock()
    mock_socket.return_value = mock_client_socket
    mock_client_socket.recv.side_effect = [
        struct.pack(">L", 10),  # Length of log record
        pickle.dumps(
            logging.LogRecord(
                name="test_logger",
                level=logging.INFO,
                pathname="",
                lineno=1,
                msg="Test log",
                args=None,
                exc_info=None,
            )
        ),
    ]

    server_instance.handle_client(mock_client_socket)

    # Ensure that the client socket received the expected calls
    mock_client_socket.recv.assert_called()


def test_log_server_logs(server):
    """Test that logs are correctly appended to the log file by LogServer."""
    server_instance, log_file, host, port = server
    logger = logging.getLogger("TestLogger")
    logger.setLevel(logging.INFO)
    handler = logging.handlers.SocketHandler(host, port)
    logger.addHandler(handler)

    logger.info("Test message for server logging")

    # Wait a moment to ensure the message is logged
    time.sleep(1)

    with open(log_file, "r") as file:
        logs = file.read()

    assert "Test message for server logging" in logs

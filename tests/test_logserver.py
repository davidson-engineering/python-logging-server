import log_server.remote_logging_app as remote_logging_app


def test_log_server_logs(logging_server, logging_config):

    for i in range(5):
        r = remote_logging_app.work(i)  # Wait a moment to ensure the message is logged

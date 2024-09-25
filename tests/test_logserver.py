import pytest
from datetime import datetime
from log_server.log_server import format_log


def test_format_log():
    payload = {
        "created": datetime.now().timestamp(),
    }
    format_log(payload)
    assert "created_human" in payload
    assert isinstance(payload["created_human"], str)
    assert len(payload["created_human"]) > 0

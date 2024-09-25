# Python Logging Server
A lightweight server to collect logs from remote clients, allowing centralized log storage for distributed applications.

## Server Configuration
A logging server can  be started by running the following command:
```python
from log_server import serve_forever

serve_forever(HOST, PORT, target="logs.txt")
```
This will start a server that listens on the specified `HOST` and `PORT`, writing all received logs to the specified file (`logs.txt`). The server will run indefinitely until manually stopped and will block the current thread.

A multithreaded server instance can be started by passing `multithreaded=True` to the `serve_forever` function. The default value is `False`.
```python
serve_forever(HOST, PORT, target="logs.txt", multithreaded=True)
```

## Client Configuration
To send logs to the server, a client can be configured as follows:

1. Retrieve or create a logger instance.
2. Create a socket handler using `logging.handlers.SocketHandler`.
3. Assign this handler to the logger.

Any logs sent to this logger will be forwarded to the logging server.
```python
import logging.handlers 
from math import factorial
import sys

# The address of the logging server
HOST, PORT = "localhost", 9001

logger = logging.getLogger("remote_logging_app")

def work(i: int) -> int:
    logger.info("Factorial %d", i)
    f = factorial(i)
    logger.info("Factorial(%d) = %d", i, f)
    return f

socket_handler = logging.handlers.SocketHandler(HOST, PORT)
stream_handler = logging.StreamHandler(sys.stderr)
logging.basicConfig(
    level=logging.INFO,
    handlers=[socket_handler, stream_handler],
)

for i in range(10):
    work(i)

logging.shutdown()
```
For more details, refer to the full client implementation in `src.log_server.remote_logging_app.py`.

## Using the `extra` Parameter

The `extra` parameter in Python's logging module allows you to pass additional contextual information with your log messages. This data is included in the payload and sent to the server, which processes and stores it along with the other log information.

To use the `extra` parameter, you can pass a dictionary of additional fields when logging a message. For example:

```python
logger = logging.getLogger("remote_logging_app")

# Log a message with additional context
logger.info("Processing item %d", 42, extra={"user_id": 1234, "operation": "process_item"})
```
The logging server will receive this extra information and write it to the log file in JSON format. For example, the server might log something like:

```json
{
    "message": "Processing item 42",
    "levelname": "INFO",
    "created": 1695651604.501,
    "created_human": "2024-09-25 12:00:04.501",
    "user_id": 1234,
    "operation": "process_item"
}
```
## Server-Side Processing of `extra`

On the server side, the additional fields passed through `extra` are simply added to the log entry payload. No special processing is done for these fields; they are logged and stored just like the other log data (e.g., `message`, `levelname`, etc.). The logging server serializes the entire log record, including any extra fields, into the log file.

This allows you to send any custom data that is relevant to your application's logging context and have it recorded by the centralized logging server.

## Making Log Time Human-Readable

The logging server automatically converts the `created` timestamp (which is in UNIX time) into a human-readable format. This is done using the `format_log` function on the server, which processes the incoming log payload before writing it to the log file.

The server adds an additional field, `created_human`, which contains the timestamp in the format `YYYY-MM-DD HH:MM:SS.mmm`. For example:

```json
{
    "message": "Factorial(5) = 120",
    "levelname": "INFO",
    "created": 1695651604.501,
    "created_human": "2024-09-25 12:00:04.501"
}
```

This ensures that timestamps in the log file are easy to read and understand, while still retaining the original `created` field for precise time calculations or further processing.
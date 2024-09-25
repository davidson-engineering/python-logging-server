# Python Logging Server
A lightweight server to collect logs from remote clients, allowing centralized log storage for distributed applications.

## Server Configuration
A logging server can  be started by running the following command:
```python
from log_server import serve_forever

serve_forever(HOST, PORT, target="logs.txt")
```
This will start a server that listens on the specified `HOST` and `PORT`, writing all received logs to the specified file (`logs.txt`). The server will run indefinitely until manually stopped and will block the current thread.

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

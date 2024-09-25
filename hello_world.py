HOST = "gfyvrmdavidson-dev"
PORT = 18845

import logging
import logging.handlers

remote_logging_handler = logging.handlers.SocketHandler(host=HOST, port=PORT)
logging.basicConfig(
    level=logging.INFO,
    handlers=[remote_logging_handler],
)

logging.info("Hello, world!", extra={"foo": "bar"})

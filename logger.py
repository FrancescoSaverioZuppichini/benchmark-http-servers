import logging

from rich.logging import RichHandler

# logging.basicConfig(
#     level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
# )
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
rich_handler = RichHandler()
stream_handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="%(message)s", datefmt="[%X]")
rich_handler.setFormatter(formatter)
logger.addHandler(rich_handler)

import logging
from redisbus.redisbus import RedisBus  # noqa: F401


FORMAT = "* %(asctime)s - %(levelname)-8s * %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

import logging

from redisbus import RedisBus


def callback(payload):
    logging.info(f"Received {payload}")


def main():
    bus = RedisBus(host="redis")
    bus.subscribe("foo.bar", callback)
    bus.start()


if __name__ == "__main__":
    main()

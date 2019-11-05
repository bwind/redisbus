import json
import sys

from redisbus import RedisBus


def main(name, payload):
    payload = json.dumps(json.loads(payload))
    RedisBus(host="redis").publish(name, payload)


if __name__ == "__main__":
    main(*sys.argv[1:])

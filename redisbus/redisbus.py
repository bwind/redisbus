import json
import logging

import redis


class RedisBus:
    def __init__(self, host=None):
        self.redis = redis.StrictRedis(host=host)
        self.pubsub = self.redis.pubsub()
        self.subscriptions = {}

    def publish(self, name, payload):
        logging.info(f"Publishing {name}: {payload}")
        self.redis.publish(name, json.dumps(payload))

    def subscribe(self, name, callback):
        self.subscriptions[name] = callback

    def start(self):
        logging.info("Starting bus...")
        self.pubsub.subscribe(*self.subscriptions.keys())
        for message in self.pubsub.listen():
            if message["type"] != "message":
                continue
            callback = self.subscriptions.get(message["channel"].decode())
            data = json.loads(message["data"].decode())
            logging.info(f"Received message: {data} intended for {callback}")

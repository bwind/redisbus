import json
import logging
import traceback


class RedisBus:
    def __init__(self, redis=None):
        self.redis = redis
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
            if callback is None:
                continue
            try:
                data = json.loads(message["data"].decode())
            except json.decoder.JSONDecodeError:
                continue
            logging.debug(f"Received message {data} for callback {callback}")
            try:
                callback(data)
            except Exception as exc:
                logging.error(f"Callback {callback} raised exception: {exc}")
                traceback.print_exc()

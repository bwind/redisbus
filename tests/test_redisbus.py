import json
import logging
from unittest import mock

from redisbus import RedisBus

logging.getLogger().setLevel(logging.DEBUG)


class TestRedisBus:
    def setup(self):
        self.channel = b"foo"
        self.data = b'{"data": [1, 2, 3]}'
        self.redis = mock.MagicMock()
        self.callback = mock.MagicMock()
        self.bus = RedisBus(redis=self.redis)
        self.bus.subscribe(self.channel.decode(), self.callback)
        self.set_data(self.data)

    def set_data(self, data):
        self.redis.pubsub.return_value.listen.return_value.__iter__.return_value = [  # noqa: E501
            {"type": "message", "channel": self.channel, "data": data}
        ]

    def test_calls_callback(self):
        self.bus.start()
        self.callback.assert_called_once_with(json.loads(self.data))

    def test_no_json_should_not_raise(self):
        self.set_data(b"asdf")
        self.bus.start()

    def test_callback_raises(self):
        self.callback.side_effect = lambda p: None.startwith(True)
        self.bus.start()

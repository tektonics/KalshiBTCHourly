import asyncio
import json
import websockets
from collections import deque
import time

class BTCPriceFeed:
    def __init__(self, window_seconds=60):
        self.prices = deque()
        self.window = window_seconds
        self.current_avg = None
        self.current_price = None

    async def connect(self):
        url = "wss://ws-feed.exchange.coinbase.com"
        async with websockets.connect(url) as ws:
            subscribe_msg = {
                "type": "subscribe",
                "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
            }
            await ws.send(json.dumps(subscribe_msg))

            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                if data["type"] == "ticker" and "price" in data:
                    price = float(data["price"])
                    timestamp = time.time()
                    self._update_prices(price, timestamp)

    def _update_prices(self, price, timestamp):
        self.prices.append((timestamp, price))
        self.current_price = price

        # Remove entries older than self.window seconds
        while self.prices and self.prices[0][0] < timestamp - self.window:
            self.prices.popleft()

        if self.prices:
            self.current_avg = sum(p for _, p in self.prices) / len(self.prices)

    def get_current_price(self):
        return self.current_price

    def get_rolling_average(self):
        return self.current_avg

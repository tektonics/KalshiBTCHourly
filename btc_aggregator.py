
import asyncio
import json
import time
from collections import deque
import websockets
import aiohttp

class RollingPriceWindow:
    def __init__(self, window_seconds=60):
        self.window = window_seconds
        self.prices = deque()

    def update(self, price):
        now = time.time()
        self.prices.append((now, price))
        self._trim(now)

    def _trim(self, now):
        while self.prices and self.prices[0][0] < now - self.window:
            self.prices.popleft()

    def average(self):
        if not self.prices:
            return None
        return sum(p for _, p in self.prices) / len(self.prices)


class BTCPriceAggregator:
    def __init__(self):
        self.coinbase = RollingPriceWindow()
        self.kraken = RollingPriceWindow()
        self.bitstamp = RollingPriceWindow()

    async def start(self):
        await asyncio.gather(
            self._coinbase_feed(),
            self._kraken_feed(),
            self._bitstamp_feed()
        )

    def get_current_average_price(self):
        prices = [
            self.coinbase.average(),
            self.kraken.average(),
            self.bitstamp.average()
        ]
        valid = [p for p in prices if p is not None]
        return sum(valid) / len(valid) if valid else None

    async def _coinbase_feed(self):
        url = "wss://ws-feed.exchange.coinbase.com"
        async with websockets.connect(url) as ws:
            await ws.send(json.dumps({
                "type": "subscribe",
                "channels": [{"name": "ticker", "product_ids": ["BTC-USD"]}]
            }))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("type") == "ticker" and "price" in msg:
                    self.coinbase.update(float(msg["price"]))

    async def _kraken_feed(self):
        url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(url) as resp:
                        data = await resp.json()
                        price = float(data["result"]["XXBTZUSD"]["c"][0])
                        self.kraken.update(price)
                except:
                    pass
                await asyncio.sleep(5)

    async def _bitstamp_feed(self):
        url = "wss://ws.bitstamp.net"
        async with websockets.connect(url) as ws:
            await ws.send(json.dumps({
                "event": "bts:subscribe",
                "data": {"channel": "live_trades_btcusd"}
            }))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("event") == "trade" and "price" in msg["data"]:
                    self.bitstamp.update(float(msg["data"]["price"]))

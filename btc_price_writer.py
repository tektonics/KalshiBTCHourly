import asyncio
import json
from btc_aggregator import BTCPriceAggregator


async def write_price(aggregator: BTCPriceAggregator, interval: int = 5, path: str = "btc_price.json"):
    """Periodically write the aggregated BTC price to a JSON file."""
    while True:
        await asyncio.sleep(interval)
        price = aggregator.get_current_average_price()
        if price is None:
            continue
        with open(path, "w") as f:
            json.dump({"price": price}, f)


async def main():
    aggregator = BTCPriceAggregator()
    # Start the price feeds in the background
    asyncio.create_task(aggregator.start())
    await write_price(aggregator)


if __name__ == "__main__":
    asyncio.run(main())

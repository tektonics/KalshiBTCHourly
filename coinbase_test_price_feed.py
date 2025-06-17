import asyncio
from coinbase_price_feed import BTCPriceFeed

async def main():
    feed = BTCPriceFeed()

    # Start the feed in background
    asyncio.create_task(feed.connect())

    # Print current and rolling average prices every 5 seconds
    while True:
        await asyncio.sleep(5)
        spot = feed.get_current_price()
        avg = feed.get_rolling_average()
        print(f"Current BTC Price: {spot}, 60s Rolling Average: {avg}")

asyncio.run(main())

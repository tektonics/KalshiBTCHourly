import asyncio
from btc_aggregator import BTCPriceAggregator

async def main():
    aggregator = BTCPriceAggregator()
    asyncio.create_task(aggregator.start())

    while True:
        await asyncio.sleep(3)
        avg = aggregator.get_current_average_price()
        print(f"Aggregated BTC Price (60s Rolling Avg): {avg}")

asyncio.run(main())

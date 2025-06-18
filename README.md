# Kalshi BTC Hourly Tools

This repository contains a simple Bitcoin price aggregator and a Kalshi API client. The aggregator collects BTC prices from several exchanges and writes the rolling average to `btc_price.json`. The client then uses this file to determine which market to subscribe to on Kalshi.

## Requirements

- Python 3.11+
- `pip install -r requirements.txt`

## 1. Setting up environment variables

Create a `.env` file in the project root. It should define the following variables:

```
KALSHI_API_KEY=<your kalshi api key>
KALSHI_PRIVATE_KEY_PATH=/path/to/your/private_key.pem
```

The Kalshi client loads this file automatically using `python-dotenv`.

## 2. Running the aggregator and Kalshi client

1. Start the BTC aggregator which writes the rolling price to `btc_price.json`:

   ```bash
   python btc_price_writer.py
   ```

   Leave this running so the price file stays up to date.

2. In another terminal, run the Kalshi client script:

   ```bash
   python test_kalshi_client.py
   ```

   The script reads `btc_price.json`, chooses the closest BTC market, and subscribes to live quotes from Kalshi.

## 3. Obtaining Kalshi credentials

1. Register for a trading account at [Kalshi](https://kalshi.com/).
2. After logging in, visit **Account Settings → API Keys** and generate a new key.
3. Download the provided RSA private key file and note the API key string.
4. Set the values in your `.env` file as shown above.

With these credentials in place and the aggregator running, the client script will authenticate with Kalshi and stream market data based on the current BTC price.

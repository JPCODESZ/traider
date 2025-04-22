# === OPTIONS-ONLY VERSION ===
import os
import time
import logging
from datetime import date, timedelta
from tradier import Tradier

# === LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# === API CONFIG ===
TRADIER_TOKEN = os.getenv("TRADIER_TOKEN") or "YOUR_TRADIER_ACCESS_TOKEN"
tradier = Tradier(access_token=TRADIER_TOKEN, endpoint="https://api.tradier.com/v1")

# === SETTINGS ===
TARGET_RETURN = 0.02   # 2% per month
DAYS_OUT = 30           # Expiration date ~30 days out
DELTA_RANGE = (0.15, 0.30)
STOCKS = ["AAPL", "MSFT", "AMZN", "GOOGL", "META"]  # Expand as needed

# === MAIN LOOP ===
def sell_put_options():
    for symbol in STOCKS:
        try:
            chains = tradier.options_chain(symbol, expiration=date.today() + timedelta(days=DAYS_OUT))
            puts = [opt for opt in chains if opt["option_type"] == "put"]

            # Filter by delta range and OTM
            valid_puts = [p for p in puts if DELTA_RANGE[0] <= abs(float(p.get("greeks", {}).get("delta", 0))) <= DELTA_RANGE[1]]
            if not valid_puts:
                continue

            best_put = sorted(valid_puts, key=lambda x: float(x["bid"]), reverse=True)[0]
            strike = best_put["strike"]
            bid = float(best_put["bid"])
            expiration = best_put["expiration_date"]

            # Place order (paper trading assumed)
            logging.info(f"SELL PUT: {symbol} {strike} @ {bid:.2f} exp {expiration}")

        except Exception as e:
            logging.error(f"Error processing {symbol}: {e}")

while True:
    sell_put_options()
    logging.info("⏳ Sleeping 10s...")
    time.sleep(10)

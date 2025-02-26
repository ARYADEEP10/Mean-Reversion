import oandapyV20
import oandapyV20.endpoints.orders as orders
import time
import pandas as pd
import subprocess
from MRS_Script import generate_trade_signal

# Connecting to API with credentials
access_token = "c6c003988b5f76af439c1cdb2e3a87eb-f07d14553d1c093e6800c93515e4e1dc"
accountID = "101-001-31111831-001"
instrument = "EUR_USD"

# Connecting to OANDA API
api = oandapyV20.API(access_token=access_token)

# Function to place trades
def place_trade(signal, units=100):
    order_type = "BUY" if signal == 1 else "SELL"
    order_data = {
        "order": {
            "instrument": instrument,
            "units": units if signal == 1 else -units,
            "type": "MARKET"
        }
    }

    print(f"Placing {order_type} order for {units} units...")

    r = orders.OrderCreate(accountID, data=order_data)
    try:
        response = api.request(r)
        print(f"Trade executed successfully: {response}")
    except Exception as e:
        print(f" Error executing trade: {e}")

# Automated Trading Loop
while True:
    print("Fetching market data using get_csv_file.py...")

    # Force new market data to be fetched
    subprocess.run(["python", "getcsvfile.py"], check=True)
    time.sleep(2)  # Ensure the file is updated before reading

    # Load latest data from CSV
    df = pd.read_csv("eur_usd_price_data.csv", parse_dates=["time"], index_col="time")
    df.index = pd.to_datetime(df.index, utc=True)  # Convert timestamps to UTC

    # print("Data Loaded. Columns before processing:", df.columns)

    df = generate_trade_signal(df)  # Apply Trading Strategy


    # Get Last Non-Zero Signal
    non_zero_signals = df[df["signal"] != 0]
    if not non_zero_signals.empty:
        latest_signal_time = pd.to_datetime(non_zero_signals.index[-1], utc=True)  # Convert to UTC
        latest_signal = non_zero_signals["signal"].iloc[-1]
    else:
        latest_signal = 0  # No valid signal

    latest_time = pd.to_datetime(df.index[-1], utc=True)  # Convert to UTC
    time_diff = latest_time - latest_signal_time  # Compute how old the signal is

    # Debug: Print timestamps
    print(f"Latest Market Data Time (UTC): {latest_time}")

    if latest_signal == 0:
        print("⏸ No trading action: Signal is 0 (No trade detected).")
        time.sleep(15)  # Wait before checking again
        continue  # Skip trade execution

    # Allow trading if signal is less than 5 minutes old
    if time_diff.total_seconds() > 2500:
        print(f"Skipping trade. Signal is too old: {time_diff.total_seconds()} seconds ago.")
        continue

    if latest_signal == 1:
        print("Buy Signal Detected!")
    elif latest_signal == -1:
        print("Sell Signal Detected!")

    # Execute Trade Only If a Valid Signal Exists
    if latest_signal in [1, -1]:
        print(f"Trade Execution Triggered: Signal {latest_signal}")
        place_trade(latest_signal)
    else:
        print("No valid trade signal detected.")

    print(f"Waiting 10 seconds before next trade check...")
    time.sleep(10)  # Wait 10 seconds before checking again


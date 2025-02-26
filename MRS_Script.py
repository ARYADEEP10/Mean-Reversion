from itertools import count

import pandas as pd

def generate_trade_signal(df):
    print("generate_trade_signal() function started...")

    df = df.copy()

    # Calculate Bollinger Bands
    df["SMA_20"] = df["close"].rolling(window=20).mean()
    df["rolling_std"] = df["close"].rolling(window=20).std()
    df["upper_band"] = df["SMA_20"] + (df["rolling_std"] * 1.8)  # Widen further
    df["lower_band"] = df["SMA_20"] - (df["rolling_std"] * 2)

    print(" Bollinger Bands calculated.")

    # Compute RSI
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=10).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=10).mean()
    rs = gain / (loss + 1e-10)
    df["RSI_5"] = 100 - (100 / (1 + rs))



    print("RSI calculated.")

    # Compute MACD (Percentage Change for More Sensitivity)
    df["EMA_12"] = df["close"].ewm(span=12, adjust=False).mean()
    df["EMA_26"] = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["MACD_Indicator"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_change"] = df["MACD"].pct_change().fillna(0)

    print("MACD calculated.")

    # Drop NaN values
    df.dropna(inplace=True)

    # Generate Trading Signals (Using MACD Percentage Change)
    df["signal"] = 0

    buy_condition = (
        (df["close"] < df["lower_band"]) &
        (df["RSI_5"] < 35) &
        (df["MACD_change"] > -0.001)  # MACD must be increasing
    )

    sell_condition = (
        (df["close"] > df["upper_band"]) &
        (df["RSI_5"] > 55) &
        (df["MACD_change"] < 0.002)  # MACD must be decreasing
    )

    df.loc[buy_condition, "signal"] = 1
    df.loc[sell_condition, "signal"] = -1

    print("Signals generated successfully.")

    # Debug: Check which rows matched Buy/Sell conditions
    print("🔍 Checking Buy Signal Conditions:")
    print(df[buy_condition].tail(5))

    print("🔍 Checking Sell Signal Conditions:")
    print(df[sell_condition].tail(5))

    # Debug: Count Buy/Sell signals
    print(f"Buy signals count: {df["signal"].astype(int).eq(1).sum()}")
    print(f"Sell signals count: {df["signal"].astype(int).eq(-1).sum()}")

    return df

# Run the function when executing the script
if __name__ == "__main__":
    print("Running MRS_Script py...")

    try:
        df = pd.read_csv("eur_usd_price_data.csv", parse_dates=["time"], index_col="time")
        print(" CSV loaded successfully.")
    except FileNotFoundError:
        print("Error: File 'eur_usd_price_data.csv' not found.")
        exit()

    df = generate_trade_signal(df)


    print(df[df['signal']!=0].tail(-50)) # Show only rows with signals


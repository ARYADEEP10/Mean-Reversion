import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from MRS_Script import generate_trade_signal


def filter_signals(df, window=10):
    """
    Filters buy/sell signals to only show significant turning points.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'signal' and 'cumulative_returns'.
        window (int): Rolling window size to determine significant signals.

    Returns:
        pd.DataFrame, pd.DataFrame: Filtered buy and sell signals.
    """
    df = df.copy()

    # Identify local maxima and minima in cumulative returns
    df["rolling_max"] = df["cumulative_returns"].rolling(window=window, center=True).max()
    df["rolling_min"] = df["cumulative_returns"].rolling(window=window, center=True).min()

    # Keep buy signals only at local lows
    buy_signals = df[(df["signal"] > df["signal"].shift(1)) & (df["cumulative_returns"] == df["rolling_min"])]

    # Keep sell signals only at local highs
    sell_signals = df[(df["signal"] < df["signal"].shift(1)) & (df["cumulative_returns"] == df["rolling_max"])]

    return buy_signals, sell_signals


# Load the data
df = pd.read_csv("eur_usd_price_data.csv", parse_dates=["time"], index_col="time")

# Apply trade signal function
df = generate_trade_signal(df)

# Compute returns
df['returns'] = df['close'].pct_change()
df['strategy_returns'] = df['signal'].shift(1) * df['returns']
df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()

# Get filtered buy/sell signals
buy_signals, sell_signals = filter_signals(df, window=10)

# Plot cumulative returns
plt.figure(figsize=(12, 8))
plt.plot(df.index, df["cumulative_returns"], label="Strategy Returns", color="blue", linewidth=2)
plt.axhline(y=1, linestyle="dashed", color="gray", linewidth=1)

# Plot filtered buy/sell markers with smaller markers
plt.scatter(buy_signals.index, buy_signals["cumulative_returns"],
            marker="^", color="green", label="Buy Signal", s=80, edgecolors='black')
plt.scatter(sell_signals.index, sell_signals["cumulative_returns"],
            marker="v", color="red", label="Sell Signal", s=80, edgecolors='black')

# Labels and legend
plt.legend()
plt.title("Cumulative Returns of Mean Reversion Strategy (Filtered Buy/Sell Signals)")
plt.xlabel("Time")
plt.ylabel("Cumulative Returns")
plt.grid(alpha=0.3)

# Show plot
plt.show()

# Print Final Performance
print(f"Final Cumulative Return: {df['cumulative_returns'].iloc[-1]:.2f}")

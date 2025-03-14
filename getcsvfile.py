import oandapyV20 as Op #python lib for connecting to panda api
import oandapyV20.endpoints.instruments as instruments #modeule to fetch historial data
import pandas as pd

# We start of by defining the API credentials
API_KEY = "c6c003988b5f76af439c1cdb2e3a87eb-f07d14553d1c093e6800c93515e4e1dc"  # Replace with your actual API key
ACCOUNT_ID = "101-001-31111831-001"  # Replace with your actual Account ID
OANDA_URL = "https://api-fxpractice.oanda.com/v3"  #OANDA API url

# Next is the instrument (currency pair) and time range
instrument = "EUR_USD" #fetches the data for Euro-USD pair
params = {
    "count": 5000, #I can also use to get the data in chunks for the year 2024 for which I have to buy license so i did not.
    "granularity": "M1"  # 1-minute candlesticks, we can also use H1, D as well
}

# Starting or initializing API client
client = Op.API(access_token=API_KEY)

# Error handling using try method and getting the historical data
try:
    request = instruments.InstrumentsCandles(instrument=instrument, params=params)
    response = client.request(request)
except Exception as e:
    print("Error fetching data:", e)
    exit()

# get the API response into a DataFrame
candles = response["candles"]

#Fetching the time and closing price from "mid price" field
data = []
for candle in candles:
    if candle["complete"]:  # To Ensure only complete candles are included
        data.append({
            "time": candle["time"],
            "open": float(candle["mid"]["o"]),  # Open price
            "high": float(candle["mid"]["h"]),  # High price
            "low": float(candle["mid"]["l"]),  # Low price
            "close": float(candle["mid"]["c"]),  # 'c' is the closing price
            "volume": candle["volume"]  # Volume of trades
        })

df = pd.DataFrame(data)

# Convert time column to datetime format
df["time"] = pd.to_datetime(df["time"])
df.set_index("time", inplace=True) #changign the index name to time

df.to_csv("eur_usd_price_data.csv")
print(df)

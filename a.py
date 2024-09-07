import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Define the ticker symbol
ticker = "AAPL"

# Get the stock data
data = yf.download(ticker, start="2020-01-01", end="2024-09-07")


# Calculate the moving average
data["MA"] = data["Close"].rolling(window=50).mean()

# Calculate the MACD
data["MACD"] = data["Close"].ewm(span=12, adjust=False).mean() - data["Close"].ewm(span=26, adjust=False).mean()

# Calculate the signal line
data["Signal"] = data["MACD"].rolling(window=9).mean()

#plot all of the data
plt.figure(figsize=(10, 6))
plt.plot(data["Close"], label="Close Price")
plt.plot(data["MA"], label="Moving Average", color="red")
plt.plot(data["MACD"], label="MACD", color="blue")
plt.plot(data["Signal"], label="Signal", color="green")
plt.title("Stock Price and Moving Average")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()


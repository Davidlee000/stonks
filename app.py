import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend

from flask import Flask, render_template, request  # Import request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])  # Allow both GET and POST
def index():
    plot_path = None  # Initialize plot_path
    if request.method == 'POST':  # Check if the request is POST
        ticker = request.form['ticker']  # Get ticker from form data

        # Get the stock data
        data = yf.download(ticker, start="2020-01-01", end="2024-09-07")

        # Check if data is empty
        if data.empty:
            return "No data found for the ticker symbol."

        # Calculate the moving average
        data["MA"] = data["Close"].rolling(window=50).mean()

        # Calculate the MACD
        data["MACD"] = data["Close"].ewm(span=12, adjust=False).mean() - data["Close"].ewm(span=26, adjust=False).mean()

        # Calculate the signal line
        data["Signal"] = data["MACD"].rolling(window=9).mean()

        # Plot all of the data
        plt.figure(figsize=(10, 6))
        plt.plot(data["Close"], label="Close Price")
        plt.plot(data["MA"], label="Moving Average", color="red")
        plt.plot(data["MACD"], label="MACD", color="blue")
        plt.plot(data["Signal"], label="Signal", color="green")
        plt.title("Stock Price and Moving Average")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()

        # Save the plot
        plot_path = os.path.join('static', 'plot.png')
        plt.savefig(plot_path)
        plt.close()

    return render_template('index.html', plot_url=plot_path)  # Render template with plot_url

if __name__ == '__main__':
    app.run(debug=True)

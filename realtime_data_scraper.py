import yfinance as yf
import csv
from datetime import datetime
from multiprocessing import Process

def get_stock_data(ticker):
    # Get the stock data
    stock = yf.Ticker(ticker)

    while True:
        # Get the historical prices for the stock
        historical_prices = stock.history()

        # Get the latest price and time
        latest_price = historical_prices['Close'].iloc[-1]
        latest_date = datetime.now().strftime("%Y-%m-%d")
        latest_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        # Write the latest stock value to the CSV file
        with open(f"{ticker}.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([ticker, latest_date, latest_time, latest_price])

        #Show the latest stock value in terminal
        print(f"{ticker},{latest_date},{latest_time},{latest_price}")

if __name__ == "__main__":
    # Get the tickers from the user
    tickers = input("Enter the stocks (separated by commas): ").split(",")

    # Run the stock data scraperin parallel, one process per ticker
    processes = []
    for ticker in tickers:
        p = Process(target=get_stock_data, args=(ticker,))
        p.start()
        processes.append(p)

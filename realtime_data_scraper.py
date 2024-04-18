import os
import yfinance as yf
import csv
from datetime import datetime
from multiprocessing import Process
import time

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    start_date = "1900-01-01"  # Fetch as much historical data as possible
    end_date = datetime.now().strftime("%Y-%m-%d")  # Today's date for the end parameter

    while True:
        # Fetch historical data and balance sheet once per day
        try:
            historical_prices = stock.history(start=start_date, end=end_date)
            historical_prices.to_csv(f"./data/historical_prices/{ticker}_historical_prices.csv")

            balance_sheet = stock.balance_sheet
            balance_sheet.to_csv(f"./data/balance_sheet/{ticker}_balance_sheet.csv")
        except Exception as e:
            print(f"Failed to fetch historical data for {ticker}: {e}")

        # Update every 24 hours
        time.sleep(86400)

def get_realtime_stock_price(ticker):
    # Function to fetch and log real-time prices continuously
    last_logged_date = None  # To track the last logged date
    while True:
        try:
            stock = yf.Ticker(ticker)
            historical_prices = stock.history(period="1d")
            latest_price = historical_prices['Close'].iloc[-1]
            latest_date = datetime.now().strftime("%Y-%m-%d")
            latest_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]

            file_exists = os.path.isfile(f"./data/realtime_prices/{ticker}_realtime_prices.csv")
            with open(f"./data/realtime_prices/{ticker}_realtime_prices.csv", "a", newline="") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Date", "Time", "Price"])
                # Only write the new date if it has changed
                if latest_date != last_logged_date:
                    writer.writerow([latest_date, latest_time, latest_price])
                    last_logged_date = latest_date
                else:
                    writer.writerow(["", latest_time, latest_price])
        except Exception as e:
            print(f"Failed to fetch real-time prices for {ticker}: {e}")

if __name__ == "__main__":
    tickers = input("Enter the stocks (separated by commas): ").split(",")

    daily_processes = []
    real_time_processes = []
    for ticker in tickers:
        p1 = Process(target=get_stock_data, args=(ticker,))
        p1.start()
        daily_processes.append(p1)

        p2 = Process(target=get_realtime_stock_price, args=(ticker,))
        p2.start()
        real_time_processes.append(p2)

    for p in daily_processes + real_time_processes:
        p.join() 

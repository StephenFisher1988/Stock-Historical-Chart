import pandas as pd
import yfinance as yf
import datetime
from datetime import date, timedelta
import plotly.graph_objects as go
import plotly.express as px

#Function to get the current stock price
def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0]

#Get today's date
today = date.today()

#Determine how far back the historical data should go.
#Replace the number after "days" to change
try:
    d1 = today.strftime("%Y-%m-%d")
    end_date = d1
    d2 = date.today() - timedelta(days=1825)
    d2 = d2.strftime("%Y-%m-%d")
    start_date = d2
except:
    print("Could not retrieve time data")

#ask the user which stock to view - self explanatory
inp = input('What stock do you wish to view? ')

#Retrieve the data
try:
    data = yf.download(inp, 
                          start=start_date, 
                          end=end_date, 
                          progress=False)
    data["Date"] = data.index
    data = data[["Date", "Open", "High", "Low", 
                 "Close", "Adj Close", "Volume"]]
    data.reset_index(drop=True, inplace=True)
    print(data.head())
except:
    print("There was an issue downloading the data")


#Build the chart
try:
    figure = px.line(data, x='Date', y='Close', 
                     title='Stock Market Prices For '+inp)

    figure.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    figure.show()
except:
    print("There was an issue loading the chart")

#In the concole, print the current price of the stock
try:
    print("The current value of", inp, "is:", get_current_price(inp))
except:
    print("Could not load current stock data")

#Allow the user to view the console data before closing
wait = input("Press ENTER to continue")

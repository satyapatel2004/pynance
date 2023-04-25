import yfinance as yf 
import inquirer
from sys import exit
import plotext
import datetime
from dateutil.relativedelta import relativedelta


#gets the stock ticker from the user: 
def get_stock():
    global tickrIn
    global tickrInfo 
    global tickr  
    
    try:
        tickrIn = input("enter your Ticker: ")
        tickr = yf.Ticker(tickrIn)

        tickrIn = tickrIn.upper() 

        #creates a dictionary with the ticker's information. 
        tickrInfo = tickr.get_info() 
        analysis() 

         
    except ImportError: 
        print("Incorrect Ticker!") 
        get_stock()

#types of analysis the user can complete (in progress)
def analysis():
    questions = [
        inquirer.List(
            "analysis", 
            message="What type of analysis do you want to do?",
            choices=["Stock Analysis", "Bar Chart", "Other2", "quit"],
        ),
    ]
    answer = inquirer.prompt(questions)

    if answer['analysis'] == "Stock Analysis":
        print(tickrInfo['sharesOutstanding'])
        stock_analysis()


    if answer['analysis'] == "Bar Chart":
        barChart() 

    if answer['analysis'] == "quit":
        get_stock() 

def barChart():

    today = datetime.date.today() 
    yrAgo = today - relativedelta(years=1)


    plotext.date_form('Y/m/d')
    end = plotext.today_datetime() 
    data = yf.download(tickrIn, yrAgo, today)

    prices = list(data["Close"])
    dates = plotext.datetimes_to_string(data.index)
    plotext.plot(dates, prices)

    plotext.title("Stock Price")
    plotext.xlabel("Date")
    plotext.ylabel("Stock price")
    plotext.show() 


#conducts the stock analysis
def stock_analysis():

    questions = [
        inquirer.List(
            "stockAnalysis", 
            message="How do you want to analyze",
            choices=["P/B", "P/E", "PEG", "Dividend Yield", "Back"],
        ),
    ]
    answer = inquirer.prompt(questions)

    if answer['stockAnalysis'] == "P/B":
        for key in tickrInfo:
            if key == 'priceToBook':
                print("the price to book ratio is " + tickrInfo[key])
    
    if answer['stockAnalysis'] == "P/E":
        for key in tickrInfo:
            if key == 'sharesOutstanding':
                outstandingShares = tickrInfo[key]

            if key == 'grossProfits':
                profit = tickrInfo[key]

            if key == 'previousClose':
                marketPrice = tickrInfo[key]

        earningsPerShare = float(outstandingShares)/float(profit) 
        print("The Price to Earnings Ratio is: " + str(float(marketPrice)/earningsPerShare))

    if answer['stockAnalysis'] == "PEG":
        for key in tickrInfo:
            if key == 'pegRatio':
                print("The PEG Ratio is " + str(tickrInfo[key]))

    if answer['stockAnalysis'] == "Dividend Yield":
        for key in tickrInfo:
            if key == 'dividendYield':
                print("the Divident Yield is " + tickrInfo[key])
                
        else: print("Dividend Yield Unavailable\n")

    if answer['stockAnalysis'] == "Back":
        analysis()
       
def main():
    get_stock()

main()

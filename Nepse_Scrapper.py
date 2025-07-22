# https://www.onlinekhabar.com/smtm/search-list/tickers

# https://www.onlinekhabar.com/smtm/ticker-page/ticker-stats/HDL

# ALTER TABLE company ADD UNIQUE(ticker, updated_on);  ---- command to add unique constraints. (Helps to avoid duplicate entries)


import requests
import pandas as pd
import mysql.connector
from Check import already_ran_today

def connect_table(database):
    
    try:
        connection=mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=database
            )
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None 
    

def add_to_table(db, table_name, data):
    cursor= db.cursor()
        
    command= f"INSERT IGNORE INTO {table_name} (ticker, ltp, point_change, percentage_change, volume, shares_traded, market_cap, updated_on) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        data['ticker'],
        data['ltp'],
        data['point_change'],
        data['percentage_change'],
        data['volume'],
        data['shares_traded'],
        data['market_cap'],
        data['updated_on']
    )
    try:
        cursor.execute(command, values)
        db.commit()
        print(f"Added {data['ticker']} to {table_name} table successfully.")
    except Exception as e:
        print(f"Error adding {data['ticker']} to table: {e}")
        db.rollback()
    finally:
        cursor.close()



def get_ticker_data():
    db=connect_table("nepse")
    if db is None:
        return
    
    if already_ran_today(db):
        print("Data for today has already been fetched.")
        db.close()
        return
    url= "https://www.onlinekhabar.com/smtm/search-list/tickers"
    try:
        req=requests.get(url)
        if req.status_code==200:
            resp=req.json()
            data=resp['response']
            for i in data:
                ticker_details= f"https://www.onlinekhabar.com/smtm/ticker-page/ticker-stats/{i['ticker']}"
                ticker_req=requests.get(ticker_details)
                if ticker_req.status_code==200:
                    ticker_data=ticker_req.json()['response']
                    ticker_data['updated_on']=f'20{ticker_data["updated_on"]}'.split(" ")[0]

                    add_to_table(
                        db,
                        'company',
                        ticker_data
                    )

                else:
                    print(f"Failed to get data for{ticker_data['ticker']} :{ticker_req.status_code}")

        else:
            print(f"Request failed with status code: {req.status_code}")
    except Exception as e:
        print(f"Error fetching data: {e}")
    
    
    db.close()

get_ticker_data()
    


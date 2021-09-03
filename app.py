from flask import Flask  
from nsepy import get_history
from datetime import datetime, timedelta
import pandas as pd
import requests
from flask import jsonify
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
  
app = Flask(__name__) #creating the Flask class object   




class NseIndia:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("http://nseindia.com", headers=self.headers)

    def pre_market_data(self):
        pre_market_key = {"NIFTY 50": "NIFTY", "Nifty Bank": "BANKNIFTY", "Emerge": "SME", "Securities in F&O": "FO",
                          "Others": "OTHERS", "All": "ALL"}
        key = "NIFTY 50"   # input
        data = self.session.get(f"https://www.nseindia.com/api/market-data-pre-open?key={pre_market_key[key]}", headers=self.headers).json()["data"]
        new_data = []
        for i in data:
            new_data.append(i["metadata"])
        df = pd.DataFrame(new_data)
        # return list(df['symbol'])
        return df

    def live_market_data(self):
        live_market_index = {
            'Broad Market Indices': ['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY MIDCAP 50', 'NIFTY MIDCAP 100',
                                     'NIFTY MIDCAP 150', 'NIFTY SMALLCAP 50', 'NIFTY SMALLCAP 100',
                                     'NIFTY SMALLCAP 250', 'NIFTY MIDSMALLCAP 400', 'NIFTY 100', 'NIFTY 200'],
            'Sectoral Indices': ["NIFTY AUTO", "NIFTY BANK", "NIFTY ENERGY", "NIFTY FINANCIAL SERVICES",
                                 "NIFTY FINANCIAL SERVICES 25/50", "NIFTY FMCG", "NIFTY IT", "NIFTY MEDIA",
                                 "NIFTY METAL", "NIFTY PHARMA", "NIFTY PSU BANK", "NIFTY REALTY",
                                 "NIFTY PRIVATE BANK"],
            'Others': ['Securities in F&O', 'Permitted to Trade'],
            'Strategy Indices': ['NIFTY DIVIDEND OPPORTUNITIES 50', 'NIFTY50 VALUE 20', 'NIFTY100 QUALITY 30',
                                 'NIFTY50 EQUAL WEIGHT', 'NIFTY100 EQUAL WEIGHT', 'NIFTY100 LOW VOLATILITY 30',
                                 'NIFTY ALPHA 50', 'NIFTY200 QUALITY 30', 'NIFTY ALPHA LOW-VOLATILITY 30',
                                 'NIFTY200 MOMENTUM 30'],
            'Thematic Indices': ['NIFTY COMMODITIES', 'NIFTY INDIA CONSUMPTION', 'NIFTY CPSE', 'NIFTY INFRASTRUCTURE',
                                 'NIFTY MNC', 'NIFTY GROWTH SECTORS 15', 'NIFTY PSE', 'NIFTY SERVICES SECTOR',
                                 'NIFTY100 LIQUID 15', 'NIFTY MIDCAP LIQUID 15']}

        # indices = "Sectoral Indices"    # input
        # key = "NIFTY FINANCIAL SERVICES 25/50"     # input
        indices ="Others"
        key = "Securities in F&O"
        data = self.session.get(f"https://www.nseindia.com/api/equity-stockIndices?index={live_market_index[indices][live_market_index[indices].index(key)].upper().replace(' ','%20').replace('&', '%26')}", headers=self.headers).json()["data"]
        df = pd.DataFrame(data)
        df = df.loc[:,["symbol","open","dayHigh","dayLow","lastPrice","previousClose","change","pChange"]]
        # return list(df["symbol"])
        df.to_csv(f"stock/live.csv")
        return df

    def holidays(self):
        holiday = ["clearing", "trading"]
        # key = input(f'Select option {holiday}\n: ')
        key = "trading"   # input
        data = self.session.get(f'https://www.nseindia.com/api/holiday-master?type={holiday[holiday.index(key)]}', headers=self.headers).json()
        df = pd.DataFrame(list(data.values())[0])
        return df




 
    def refresh():
        nifty=pd.read_csv('fno.csv')
        current_data=[]
        for index, row in nifty.iterrows():
            symbol=row["SYMBOL"]
            d = datetime.today()
            day=datetime.now().day
            month=datetime.now().month
            year=datetime.now().year
            df=get_history(symbol,start=datetime(d.year,d.month,d.day),end=datetime(year,month,day))
            data=pd.DataFrame(df)
            print(df)
            if data.shape[0]>1:
                print(data["Symbol"][0])
                oprice=data["Open"][0]
                high=data["High"][0]
                low=data["Low"][0]
                last=data["Last"][0]
                close=data["Close"][0]
                
                list=[]
                list.append(data["Symbol"][0])
                list.append(oprice)
                list.append(high)
                list.append(low)
                list.append(last)
                list.append(close)
                current_data.append(list)
            print(current_data)
            data = pd.DataFrame(current_data, columns =['Symbol', 'Open', 'High','Low','Last','Close'])
            data.to_csv(f"stock/point00.csv")
            # data.to_csv(f"stock/{symbol}.csv")
            # try:
            
            #     symbol=row["Symbol"]
            #     d = datetime.today() - timedelta(days=1)
            #     day=datetime.now().day
            #     month=datetime.now().month
            #     year=datetime.now().year
            #     df=get_history(symbol,start=datetime(d.year,d.month,d.day),end=datetime(year,month,day))
            #     data=pd.DataFrame(df)
            #     data.to_csv(f"stocks/{symbol}.csv")
                
            # except:
            #     print("exception occur")



@app.route('/') #decorator drfines the   
def home():  
    return "Server is running on  localhost:5000";
    
@app.route('/live') #decorator drfines the   
def live():  
    #refresh()
    nse = NseIndia()
    df=nse.live_market_data()
    df_list = df.values.tolist()
    JSONP_data = jsonify(df_list)
    return JSONP_data

    # print(nse.pre_market_data())
    #print(nse.live_market_data())
    # print(nse.holidays())
    #return jsonify(df);  
  
if __name__ =='__main__':  
    app.run(debug = True)  
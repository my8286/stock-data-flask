from flask import Flask  
from nsepy import get_history
from datetime import datetime, timedelta
import pandas as pd
  
app = Flask(__name__) #creating the Flask class object   
 
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
    refresh()
    return "hello, this is our first flask website";  
  
if __name__ =='__main__':  
    app.run(debug = True)  
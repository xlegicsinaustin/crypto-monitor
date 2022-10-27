import pandas as pd
import numpy as np
import yfinance as yf
import sqlalchemy as sql
import unicorn_binance_websocket_api as unicorn
import json
__all__ = [
    'pd',
    'np',
    'yf',
    'sql',
    'unicorn',
    'json'
]

class data_retrieval:

    def __init__(self):
        pass

    def open_db():
        """
        open the database
        """
        engine = sql.create_engine('sqlite:///Liveprice.db')
        return engine

    def SQLimport(data,engine):
        """
        function to import the live data into our database
        """
        time = pd.to_datetime(data['event_time'],unit='ms')
        close = float(data['kline']['close_price'])
        frame = pd.DataFrame({'timestamp':time,'price':close},index=[0])
        frame.to_sql(data['symbol'],engine,index=False,if_exists='append')
        
    def get_live_price(engine):
        """
        get live price of asset
        """
        #creating live stream for data
        ubwa = unicorn.BinanceWebSocketApiManager(exchange='binance.com')

        # live stream data interval 1 minute 
        ubwa.create_stream('kline_1m', 'MATICUSDT',output='UnicornFy')

        data = ubwa.pop_stream_data_from_stream_buffer()

        #import data from the stream
        while True:
            data = ubwa.pop_stream_data_from_stream_buffer()
            if data and len(data) >3:
                data_retrieval.SQLimport(data,engine)

    def get_historic_price():
        """
        get historic price data via yahoo finance
        """
        
        asset = ['BTC-USD']
        asset_data = yf.download(asset,start='2022-01-01')
        return asset_data
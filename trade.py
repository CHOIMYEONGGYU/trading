import pybithumb
import time
import datetime


con_key = ""
sec_key = ""

bithumb = pybithumb.Bithumb(con_key, sec_key)

def get_yesterday_ma5(ticker):
     df = pybithumb.get_ohlcv(ticker)
     close = df['close']
     ma = close.rolling(window=5).mean()
     return ma[-2]

def get_target_price(ticker):
     df = pybithumb.get_ohlcv(ticker)
     yesterday = df.iloc[-2]
     today_open = yesterday['close']
     yesterday_high = yesterday['high']
     yesterday_low = yesterday['low']
     target = today_open + (yesterday_high - yesterday_low) * 0.5
     return target

def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit =krw*0.7/float(sell_price)
    bithumb.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma5 = get_yesterday_ma5("ARW")
target_price = get_target_price("ARW")

while True:
    try:
        now = datetime.datetime.now()
        if mid <= now <= mid + datetime.timedelta(seconds=10):
            target_price = get_target_price("ARW")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            ma5 = get_yesterday_ma5("ARW")
            sell_crypto_currency("ARW")

        current_price = pybithumb.get_current_price("ARW")
        if (current_price > target_price) and (current_price > ma5):
            buy_crypto_currency("ARW")

    except:
        print("에러발생")

    time.sleep(1)

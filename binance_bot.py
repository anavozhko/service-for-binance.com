from binance.client import Client
from binance.websockets import BinanceSocketManager
from settings import BINANCE_API_KEY, BINANCE_API_SECRET
from twisted.internet import reactor
from database import Database
from telegram import bot
from datetime import datetime
import time


def process_message(msg):
    db = Database()
    db.write_price(float(msg['p']))
    db.close()


if __name__ == '__main__':

    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
    database = Database()
    database.create_tables()

    bm = BinanceSocketManager(client)
    conn_key = bm.start_trade_socket('BNBBTC', process_message)
    bm.start()

    try:
        while True:
            time.sleep(35)
            min_price = database.get_min_price()
            max_price = database.get_max_price()
            if min_price and max_price:
                diff = 100 - min_price * 100 / max_price
                if diff > 0.5:
                    # send message
                    chats_id = database.get_chats_id()
                    for chat_id in chats_id:
                        bot.send_message(chat_id, min_price)
                    # write the lowest price to db
                    # check_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # database.write_lowest_price(check_time, min_price)
            database.clear_prices()

    except KeyboardInterrupt:
        exit()

    bm.stop_socket(conn_key)
    bm.close()
    database.close()
    reactor.stop()

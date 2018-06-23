import psycopg2
from settings import DB_CONN_STRING


class Database(object):
    """ This class is for working with a database """
    def __init__(self):
        # Connect to the database server
        try:
            self.conn = psycopg2.connect(DB_CONN_STRING)
            self.cursor = self.conn.cursor()
        except (Exception, psycopg2.DatabaseError) as error:
            print error

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def create_tables(self):
        """ create tables in the database"""
        commands = (
            'CREATE TABLE IF NOT EXISTS prices (price NUMERIC(8,8))',
            'CREATE TABLE IF NOT EXISTS lowest_prices (date TIMESTAMP, price NUMERIC(8,8))',
            'CREATE TABLE IF NOT EXISTS chats_id (chat_id VARCHAR(15))')
        try:
            for command in commands:
                self.cursor.execute(command)
                self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print error

    def write_chat_id(self, chat_id):
        self.cursor.execute("SELECT chat_id FROM chats_id WHERE chat_id = '%s'",
                            (chat_id,))
        row = self.cursor.fetchone()
        if not row:
            self.cursor.execute('INSERT INTO chats_id (chat_id) VALUES(%s)',
                                (chat_id,))
            self.conn.commit()

    def get_chats_id(self):
        self.cursor.execute('SELECT chat_id FROM chats_id')
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def delete_chat_id(self, chat_id):
        self.cursor.execute("DELETE FROM chats_id WHERE chat_id = '%s'",
                            (chat_id,))
        self.conn.commit()

    def write_price(self, price):
        self.cursor.execute('INSERT INTO prices (price) VALUES(%s)',
                            (price,))
        self.conn.commit()

    def write_lowest_price(self, date, price):
        self.cursor.execute('INSERT INTO lowest_prices (date, price) '
                            'VALUES(%s, %s)', (date, price,))
        self.conn.commit()

    def get_max_price(self):
        self.cursor.execute('SELECT MAX(price) FROM prices')
        row = self.cursor.fetchone()
        if not row:
            return 0
        else:
            return row[0]

    def get_min_price(self):
        self.cursor.execute('SELECT MIN(price) FROM prices')
        row = self.cursor.fetchone()
        if not row:
            return 0
        else:
            return row[0]

    def clear_prices(self):
        self.cursor.execute('DELETE FROM prices')
        self.conn.commit()

    def clear_lowest_prices(self):
        self.cursor.execute('DELETE FROM lowest_prices')
        self.conn.commit()

    def clear_chats_id(self):
        self.cursor.execute('DELETE FROM chats_id')
        self.conn.commit()

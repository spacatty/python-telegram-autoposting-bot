import sqlite3
import jsonpickle
from logger import logger

class DBController:
    def __init__(self) -> None:
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()
    def init_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Messages ( id INTEGER PRIMARY KEY, message TEXT NOT NULL, channel TEXT NOT NULL, sent INT DEFAULT 0, object TEXT NOT NULL)")
        self.connection.commit()
    def is_unique_message(self, message, channel):
        self.cursor.execute(f"SELECT * FROM Messages WHERE message = '{message.id}' AND channel = '{channel}'")
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            return False
        return True
    def add_message(self, message, channel):
        try:
            self.cursor.execute(f"INSERT INTO Messages (message, channel, object) VALUES ('{message.id}', '{channel}', '{jsonpickle.encode(message)}')")
            self.connection.commit()
        except Exception as e:
            logger.error(e)
    def get_unsent_messagess(self):
        self.cursor.execute(f"SELECT * FROM Messages WHERE sent = 0")
        rows = self.cursor.fetchall()
        return rows
    def update_message_status(self, message_id):
        self.cursor.execute(f"UPDATE Messages SET sent = 1 WHERE id = {message_id}")
        self.connection.commit()
    def close_connection(self):
        self.connection.close()

import sqlite3
import sys
import os

class DatabaseManager:
    #Constructor
    def __init__(self, db_name="stardew_valley.db"):
        self.db_name = db_name
        self.conn = None #Not instantiated as "None" as NO connection
        self.cursor = None# is made until necessary

    #Open a connection only if one is NOT already open
    def open_connection(self):
        if not self.conn:
            db_path = self.get_db_path(self.db_name)
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()         
    #Closes a connection, only if one is ALREADY open
    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
            
    #Opens a connection, fetches one value, closes connection
    def fetch_one(self, query, params=()):
        self.open_connection()
        self.cursor.execute(query, params)
        result = self.cursor.fetchone()
        self.close_connection()
        return result

    def fetch_all(self, query, params=()):
        self.open_connection()
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        self.close_connection()
        return result

    #Execute an INSERT/UPDATE/DELETE query
    def execute_query(self, query, params=()):
        self.open_connection()
        self.cursor.execute(query, params)
        self.conn.commit()
        self.close_connection()

    def get_db_path(self, filename):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, filename)
        
        
        
        




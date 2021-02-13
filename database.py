import psycopg2
import json

from config import Configuration


class Database:
    def __init__(self):
        print("girdi")
        self.config = Configuration("config.json").config["database"]
        """print(self.config["host"])
        print(self.config["user"])
        print(self.config["password"])"""
        self.connection = psycopg2.connect("host={0} user={1} dbname={2} password={3} sslmode={4} "
                                           .format(self.config["host"],
                                                   self.config["user"],
                                                   self.config["dbname"],
                                                   self.config["password"],
                                                   self.config["ssl"]))

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()
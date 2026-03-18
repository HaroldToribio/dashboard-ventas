import mysql.connector
from contextlib import contextmanager

class DatabaseConnection:

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Lalito300*",
            database="inventariosimulacion"
        )
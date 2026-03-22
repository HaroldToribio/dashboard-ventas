import mysql.connector
import os

class DatabaseConnection:
    """
    Configurar antes de correr la app:
        export DB_HOST=localhost
        export DB_USER=root
        export DB_PASSWORD=tu_password
        export DB_NAME=inventariosimulacion
    """

    def get_connection(self):
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "Lalito300*"),
            database=os.getenv("DB_NAME", "inventariosimulacion")
        )
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def getConexao():
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DB_SERVER_ADV')},{os.getenv('DB_PORT_ADV')};"
            f"DATABASE={os.getenv('DB_DATABASE_ADV')};"
            f"UID={os.getenv('DB_USER_ADV')};"
            f"PWD={os.getenv('DB_PASSWORD_ADV')}"
        )
        return conn

def getConexaoE():
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={os.getenv('DB_SERVER_EXCEL')},{os.getenv('DB_PORT_EXCEL')};"
            f"DATABASE={os.getenv('DB_DATABASE_EXCEL')};"
            f"UID={os.getenv('DB_USER_EXCEL')};"
            f"PWD={os.getenv('DB_PASSWORD_EXCEL')}"
        )
        return conn

import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv(dotenv_path='.env')

db_config = {
    'host': os.getenv('host'),
    'port': os.getenv('port'),
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'database': os.getenv('database')

}
def connect_db():
    conn = mysql.connector.connect(**db_config)
    return conn

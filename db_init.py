import mysql.connector 
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

mydb = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS universaltranslatedb")
mycursor.execute("USE universaltranslatedb")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS API_Gestion_Key (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    discord_id VARCHAR(50) NOT NULL,
    api_key VARCHAR(32) NOT NULL,
    active BOOLEAN NOT NULL,
    status VARCHAR(255) NOT NULL
)
""")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS API_request (
    id INT AUTO_INCREMENT PRIMARY KEY,
    uuid VARCHAR(255) NOT NULL,
    api_key VARCHAR(100) NOT NULL,
    serveur VARCHAR(255),   
    date_used DATETIME NOT NULL,
    message TEXT,
    input_language VARCHAR(6),
    output_language VARCHAR(6) NOT NULL
)
""")

mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)

print(mydb)

mydb.close()

import mysql.connector
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def check_uuid_in_db(uuid_to_check, username, discord_id, active, status):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cursor = connection.cursor()
        query = "SELECT * FROM api_gestion_key WHERE api_key = %s"
        cursor.execute(query, (uuid_to_check,))

        # Si l'UUID est présent dans la base de données
        if cursor.fetchone():
            print("L'UUID est déjà dans la base de données.")
        else:
            insert_into_db(username, discord_id, uuid_to_check, active, status)

    except mysql.connector.Error as error:
        print("Erreur lors de la requête dans la base de données :", error)

    finally:
        if 'connection' in locals() or 'connection' in globals():
            cursor.close()
            connection.close()

def insert_into_db(username, discord_id, api_key, active, status):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = connection.cursor()
        query = "INSERT INTO api_gestion_key (username, discord_id, api_key, active, status) VALUES (%s, %s, %s, %s, %s)"
        data = (username, discord_id, api_key, active, status)
        cursor.execute(query, data)
        connection.commit()
        print("Données insérées avec succès dans la base de données.")

    except mysql.connector.Error as error:
        print("Erreur lors de l'insertion dans la base de données :", error)

# Collecte des informations depuis la console
username = input("Entrez le nom d'utilisateur : ")
discord_id = input("Entrez l'identifiant Discord : ")
active = input("Entrez 'True' pour actif ou 'False' pour inactif : ").lower() == 'true'
status = input("Entrez le statut : ")

# Générer l'UUID
generated_uuid = 'UTM' + str(uuid.uuid4()).replace('-', '')[:29]
print(username)
print(discord_id)
print(active)
print(status)
print(generated_uuid)

check_uuid_in_db(generated_uuid, username, discord_id, active, status)

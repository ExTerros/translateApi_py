from flask import Flask, request, jsonify
from googletrans import Translator
import logging
import datetime
import os
from dotenv import load_dotenv
import re
import mysql.connector

LANGUAGES = [
    'auto',
    'af',
    'sq',
    'am',
    'ar',
    'hy',
    'az',
    'eu',
    'be',
    'bn',
    'bs',
    'bg',
    'ca',
    'ceb',
    'ny',
    'zh-cn',
    'zh-tw',
    'co',
    'hr',
    'cs',
    'da',
    'nl',
    'en',
    'eo',
    'et',
    'tl',
    'fi',
    'fr',
    'fy',
    'gl',
    'ka',
    'de',
    'el',
    'gu',
    'ht',
    'ha',
    'haw',
    'iw',
    'he',
    'hi',
    'hmn',
    'hu',
    'is',
    'ig',
    'id',
    'ga',
    'it',
    'ja',
    'jw',
    'kn',
    'kk',
    'km',
    'ko',
    'ku',
    'ky',
    'lo',
    'la',
    'lv',
    'lt',
    'lb',
    'mk',
    'mg',
    'ms',
    'ml',
    'mt',
    'mi',
    'mr',
    'mn',
    'my',
    'ne',
    'no',
    'or',
    'ps',
    'fa',
    'pl',
    'pt',
    'pa',
    'ro',
    'ru',
    'sm',
    'gd',
    'sr',
    'st',
    'sn',
    'sd',
    'si',
    'sk',
    'sl',
    'so',
    'es',
    'su',
    'sw',
    'sv',
    'tg',
    'ta',
    'te',
    'th',
    'tr',
    'uk',
    'ur',
    'ug',
    'uz',
    'vi',
    'cy',
    'xh',
    'yi',
    'yo',
    'zu']

load_dotenv()

MY_IP = os.getenv('MY_IP')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
MOD_VERSION_FORGE = os.getenv('MOD_VERSION_FORGE')
MOD_VERSION_FABRIC = os.getenv('MOD_VERSION_FABRIC')

def add_space_after_punctuation(text):
    return re.sub(r'([?.])(?!\s|$)', r'\1 ', text)

app = Flask(__name__)
translator = Translator()

log_directory = 'log'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

current_datetime = datetime.datetime.now()
log_filename = f"{log_directory}/app_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.log"

with open(log_filename, 'a', encoding='utf-8') as f:
    pass

logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_user_token(token):
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = db.cursor()

        query = "SELECT active FROM api_gestion_key WHERE api_key = %s AND active = true"
        cursor.execute(query, (token,))
        result = cursor.fetchone()

        db.close()

        if result:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Erreur lors de la connexion à la base de données:", err)
        return False
    
def add_api_request(uuid, api_key, serveur, date_used, message, input_language, output_language):
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = db.cursor()

        query = """
        INSERT INTO api_request (uuid, api_key, serveur, date_used, message, input_language, output_language)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (uuid, api_key, serveur, date_used, message, input_language, output_language))

        db.commit()

        db.close()

        print("Nouvelle entrée ajoutée avec succès.")
        return True
    except mysql.connector.Error as err:
        print("Erreur lors de l'ajout de l'entrée:", err)
        return False
    
@app.route('/get', methods=['GET'])
def translate_text():
    api_key = request.args.get('key')
    text_to_translate = request.args.get('q')
    destination_lang = request.args.get('dest')
    uuid = request.args.get('uuid')
    server_ip = request.args.get('serv_ip')
    source_lang = request.args.get('src')

    print(server_ip)

    log_info = f"-----------------------------------------------------------------------------------"
    logging.info(log_info)  

    if not check_user_token(api_key):
        log_info = f"Erreur: 'Unauthorized access'"
        logging.info(log_info)
        print(api_key)
        print("Erreur: 'Unauthorized access'")
        return jsonify({'error': 'Unauthorized access'}), 200

    if text_to_translate is None or destination_lang is None:
        log_info = f"Erreur: 'Missing parameters'"
        logging.info(log_info)

        print("Erreur: 'Missing parameters'")

        return jsonify({'error': 'Missing parameters'}), 200
        
    if source_lang not in LANGUAGES:
        log_info = f"Erreur: 'Source language not supported or nonexistent.'"
        logging.info(log_info)
        print("Erreur: 'Source language not supported or nonexistent.'")
        return jsonify({'error': 'Source language not supported or nonexistent.'}), 200

    if destination_lang not in LANGUAGES:
        log_info = f"Erreur: 'Destination language not supported or nonexistent.'"
        logging.info(log_info)
        print("Erreur: 'Destination language not supported or nonexistent.'")
        return jsonify({'error': 'Destination language not supported or nonexistent.'}), 200
    
    if source_lang == "auto":
        source_lang = None

    if source_lang is not None:
        translated_text = translator.translate(text_to_translate, src=source_lang, dest=destination_lang)
        log_info = f"Entrée: {text_to_translate}, Lang_Sortie: {translated_text.dest}, Lang_Source: {translated_text.src}, Sortie: {translated_text.text}"
        logging.info(log_info)
    else:
        translated_text = translator.translate(text_to_translate, dest=destination_lang)
        log_info = f"Entrée: {text_to_translate}, Lang_Sortie: {translated_text.dest}, Lang_Source: {translated_text.src}, Sortie: {add_space_after_punctuation(translated_text.text)}"
        logging.info(log_info)

    add_api_request(uuid, api_key, server_ip, datetime.datetime.now(), text_to_translate, source_lang, destination_lang)

    print(f"Entrée: {text_to_translate}, Lang_Sortie: {translated_text.dest}, Lang_Source: {translated_text.src}, Sortie: {add_space_after_punctuation(translated_text.text)}")

    return jsonify({'translation': add_space_after_punctuation(translated_text.text), 'src': translated_text.src, 'dest': translated_text.dest}), 200 

@app.route('/check_api_key', methods=['GET'])
def check_token():
    api_key = request.args.get('key')
    print(check_user_token(api_key))
    return jsonify({'status': check_user_token(api_key)})

@app.route('/get_mod_forge_version', methods=['GET'])
def mod_forge_version():
    client_version = request.args.get('v')

    log_info = f"-----------------------------------------------------------------------------------"
    logging.info(log_info)

    if client_version != MOD_VERSION_FORGE:
        log_info = f"Update: 'False'"
        logging.info(log_info)

        print("Update: 'False'")

        return jsonify({'update': False})
    
    if client_version == MOD_VERSION_FORGE:
        log_info = f"Update: 'True'"
        logging.info(log_info)

        print("Update: 'True'")

        return jsonify({'update': True })
    
    
@app.route('/get_mod_fabric_version', methods=['GET'])
def mod_fabric_version():
    client_version = request.args.get('v')

    log_info = f"-----------------------------------------------------------------------------------"
    logging.info(log_info)

    if client_version != MOD_VERSION_FABRIC:
        log_info = f"Update: 'False'"
        logging.info(log_info)

        print("Update: 'False'")

        return jsonify({'update': False})
    
    if client_version == MOD_VERSION_FABRIC:
        log_info = f"Update: 'True'"
        logging.info(log_info)

        print("Update: 'True'")

        return jsonify({'update': True})
    
@app.route('/get_language', methods=['GET'])
def get_languages_available():

    log_info = f"-----------------------------------------------------------------------------------"
    logging.info(log_info)

    log_info = f"Info: 'fr, en, es, pt'"
    logging.info(log_info)

    print("Info: 'fr, en, es, pt'")

    return jsonify({'Info': 'fr, en, es, pt'})
    
if __name__ == '__main__':
    app.run(host=MY_IP, port=3000)

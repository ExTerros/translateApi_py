from flask import Flask, request, jsonify
from googletrans import Translator
import logging
import datetime
import os
from dotenv import load_dotenv
import re

load_dotenv()

MY_IP = os.getenv('MY_IP')
TOKEN_PLAYER = os.getenv('TOKEN_PLAYER')
TOKEN_DEV = os.getenv('TOKEN_DEV')
MOD_VERSION_FORGE = os.getenv('MOD_VERSION_FORGE')
MOD_VERSION_FABRIC = os.getenv('MOD_VERSION_FABRIC')

def add_space_after_punctuation(text):
    return re.sub(r'([?.])(?!\s|$)', r'\1 ', text)

app = Flask(__name__)
translator = Translator()

# Dictionnaire de clés API autorisées
api_keys = {
    TOKEN_DEV: True,  # Dev Key
    TOKEN_PLAYER: True  # Session test key
}

# Créer le répertoire de logs s'il n'existe pas
log_directory = 'log'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Obtenir la date et l'heure actuelles pour le nom du fichier de log
current_datetime = datetime.datetime.now()
log_filename = f"{log_directory}/app_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.log"

# Ouvrir le fichier de log avec un encodage spécifié
with open(log_filename, 'a', encoding='utf-8') as f:
    pass  # Permet juste de créer le fichier s'il n'existe pas encore

# Configuration du logging en utilisant le fichier de log ouvert précédemment
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_api_key(key):
    return api_keys.get(key, False)

@app.route('/get', methods=['GET'])
def translate_text():
    api_key = request.args.get('key')
    text_to_translate = request.args.get('q')
    destination_lang = request.args.get('dest')
    source_lang = request.args.get('src')

    log_info = f"-----------------------------------------------------------------------------------"
    logging.info(log_info)  

    if api_key is None or not validate_api_key(api_key):
        log_info = f"Erreur: 'Invalid API key'"
        logging.info(log_info)

        print("Erreur: 'Invalid API key'")

        return jsonify({'error': 'Invalid API key'}), 200

    if text_to_translate is None or destination_lang is None:
        log_info = f"Erreur: 'Missing parameters'"
        logging.info(log_info)

        print("Erreur: 'Missing parameters'")

        return jsonify({'error': 'Missing parameters'}), 200

    if source_lang is not None:
        translated_text = translator.translate(text_to_translate, src=source_lang, dest=destination_lang)
        log_info = f"Entrée: {text_to_translate}, Lang_Sortie: {translated_text.dest}, Lang_Source: {translated_text.src}, Sortie: {translated_text.text}"
        logging.info(log_info)
    else:
        translated_text = translator.translate(text_to_translate, dest=destination_lang)
        log_info = f"Entrée: {text_to_translate}, Lang_Sortie: {translated_text.dest}, Lang_Source: {translated_text.src}, Sortie: {add_space_after_punctuation(translated_text.text)}"
        logging.info(log_info)

    print(f"Entrée: {text_to_translate}, Lang_Sortie: {translated_text.dest}, Lang_Source: {translated_text.src}, Sortie: {add_space_after_punctuation(translated_text.text)}")

    return jsonify({'translation': add_space_after_punctuation(translated_text.text), 'src': translated_text.src, 'dest': translated_text.dest}), 200 


@app.route('/get_mod_forge_version', methods=['GET'])
def mod_forge_version():
    client_version = request.args.get('v')

    log_info = f"-----------------------------------------------------------------------------------"
    logging.info(log_info)

    if client_version != MOD_VERSION_FORGE:
        log_info = f"Update: 'The mod have a new update'"
        logging.info(log_info)

        print("Update: 'The mod have a new update'")

        return jsonify({'update': 'The mod have a new update'})
    
    if client_version == MOD_VERSION_FORGE:
        log_info = f"Update: 'The mod is up to date'"
        logging.info(log_info)

        print("Update: 'The mod is up to date'")

        return jsonify({'update': 'The mod is up to date'})
    
    
@app.route('/get_mod_fabric_version', methods=['GET'])
def mod_fabric_version():
    client_version = request.args.get('v')

    log_info = f"-----------------------------------------------------------------------------------"
    logging.info(log_info)

    if client_version != MOD_VERSION_FABRIC:
        log_info = f"Update: 'The mod have a new update'"
        logging.info(log_info)

        print("Update: 'The mod have a new update'")

        return jsonify({'update': 'The mod have a new update'})
    
    if client_version == MOD_VERSION_FABRIC:
        log_info = f"Update: 'The mod is up to date'"
        logging.info(log_info)

        print("Update: 'The mod is up to date'")

        return jsonify({'update': 'The mod is up to date'})
    
if __name__ == '__main__':
    app.run(host=MY_IP, port=3000)

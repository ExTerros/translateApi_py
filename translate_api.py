from flask import Flask, request, jsonify
from googletrans import Translator
import logging
import datetime
import os

app = Flask(__name__)
translator = Translator()

# Dictionnaire de clés API autorisées
api_keys = {
    "HJ3dy&GMiK^h6ii": True,  # Dev Key
    "VFu%ntZ9WK7K%79": True  # Session test key
}

# Créer le répertoire de logs s'il n'existe pas
log_directory = 'log'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Obtenir la date et l'heure actuelles pour le nom du fichier de log
current_datetime = datetime.datetime.now()
log_filename = f"{log_directory}/app_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.log"

# Configuration de la journalisation avec le chemin complet du fichier
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

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

        return jsonify({'error': 'Invalid API key'}), 401

    if text_to_translate is None or destination_lang is None:
        log_info = f"Erreur: 'Missing parameters'"
        logging.info(log_info)

        return jsonify({'error': 'Missing parameters'}), 400

    if source_lang is not None:
        translated_text = translator.translate(text_to_translate, src=source_lang, dest=destination_lang)
        log_info = f"Entrée: {text_to_translate}, Lang_Sortie: {translated_text.dest}, Lang_Source: {translated_text.src}, Sortie: {translated_text.text}"
        logging.info(log_info)
    else:
        translated_text = translator.translate(text_to_translate, dest=destination_lang)
        log_info = f"Entrée: {text_to_translate}, Lang_Sortie: {translated_text.dest}, Lang_Source: {translated_text.src}, Sortie: {translated_text.text}"
        logging.info(log_info)

    return jsonify({'translation': translated_text.text, 'src': translated_text.src, 'dest': translated_text.dest}), 200 

if __name__ == '__main__':
    app.run(host='192.168.1.18', port=3000)

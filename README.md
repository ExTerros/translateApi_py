# Translate API

L'API de Traduction est un service Flask utilisant l'API Google Translate pour traduire du texte.

## Prérequis

Assurez-vous d'avoir Python installé sur votre système.

## Installation

1. Clonez ce dépôt.
2. Créez un environnement virtuel.
3. Installez les paquets requis avec `pip install -r requirements.txt`.
4. Configurez vos variables d'environnement dans un fichier `.env` suivant le format spécifié dans `.env.example`.
5. Créez un dossier `log`.

## Utilisation

1. Lancez l'application Flask en exécutant `python translate_api.py`.
2. Accédez à l'API via les routes définies.

### Routes

- **GET /get**

  Cette route gère les demandes de traduction.

  **Paramètres :**
  - `key` : Clé d'API pour l'autorisation.
  - `q` : Texte à traduire.
  - `dest` : Langue de destination pour la traduction.
  - `src` (optionnel) : Langue source du texte.

- **GET /get_mod_version**

  Cette route vérifie la version actuelle du mod.

  **Paramètres :**
  - `v` : Version du client.

### Réponse

Les réponses contiennent du JSON avec le texte traduit, la langue source et la langue de destination.

## Variables d'Environnement

- `MY_IP` : Adresse IP pour héberger le service.
- `TOKEN_PLAYER` : Clé d'API pour les sessions des joueurs.
- `TOKEN_DEV` : Clé d'API à des fins de développement.
- `MOD_VERSION` : Version actuelle du mod.

## Notes

- Assurez-vous d'utiliser des clés d'API valides pour des demandes de traduction réussies.
- Veillez à inclure tous les paramètres requis pour des traductions précises.
- Les routes et les paramètres ont été mis à jour pour correspondre aux dernières modifications du code.

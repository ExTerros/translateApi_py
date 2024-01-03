# API de Traduction

L'API de Traduction est un service basé sur Flask qui utilise l'API Google Translate pour fournir des fonctionnalités de traduction de texte.

## Prérequis

Assurez-vous d'avoir Python installé sur votre système.

## Installation

1. Clonez ce dépôt.
2. Créez un environnement virtuel.
3. Installez les paquets requis avec `pip install -r requirements.txt`.
4. Configurez vos variables d'environnement dans un fichier `.env` en suivant le format spécifié dans `.env.example`.
5. Créez un dossier `log`.

## Utilisation

1. Lancez l'application Flask en exécutant `python translate_api.py`.
2. Accédez à l'API en utilisant les routes définies.

### Routes

- **GET /get**

  Cette endpoint gère les demandes de traduction.

  **Paramètres :**
  - `key` : Clé d'API pour l'autorisation.
  - `q` : Texte à traduire.
  - `dest` : Langue de destination pour la traduction.
  - `src` (optionnel) : Langue source du texte.
  - `v` : Version du client.

### Réponse

L'endpoint répond avec du JSON contenant le texte traduit, la langue source et la langue de destination.

## Variables d'Environnement

- `MY_IP` : Adresse IP pour héberger le service.
- `TOKEN_PLAYER` : Clé d'API pour les sessions des joueurs.
- `TOKEN_DEV` : Clé d'API à des fins de développement.
- `MOD_VERSION` : Version actuelle du mod.

## Exemple

```bash
curl -X GET 'http://192.168.1.18:3000/get?key=VOTRE_CLÉ_API&q=Bonjour&dest=fr&src=en&v=0.2.11'
```

## Notes
- Assurez-vous d'utiliser des clés d'API valides pour des demandes de traduction réussies.
- Veillez à inclure tous les paramètres requis pour des traductions précises.
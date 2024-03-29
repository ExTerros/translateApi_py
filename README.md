# Universal Translation Mod

Universal Translation Mod is a Minecraft mod that allows players to translate text on signs into their desired language among FR, EN, PT, and ES.

## Features

- **User Registration:** New users can be added using the `add_new_user.py` script, which generates a unique UUID and adds user details to the database.
- **Database Initialization:** The `db_init.py` script initializes the MySQL database with necessary tables for user management and API requests.
- **Translation API:** The `translate_api.py` script has been updated to include MySQL integration for improved security and user tracking.
  - Supports translation between various languages from a predefined list.
  - Validates API key and logs translation requests to the database.

## Getting Started

1. Install the required Python libraries listed in `requirements.txt`.
2. Make a log folder
3. Run `db_init.py` to initialize the MySQL database.
4. Use `add_new_user.py` to add new users with a unique UUID.
5. Start the translation API with `translate_api.py`.
6. Check the available API routes for translation and version checks.

## API Routes

- `/get`: Translates text based on provided parameters (API key, source text, destination language, etc.).
- `/check_api_key`: Checks the validity of the API key.
- `/get_mod_forge_version` and `/get_mod_fabric_version`: Checks for updates in Forge and Fabric versions.
- `/get_language`: Retrieves available languages for translation.

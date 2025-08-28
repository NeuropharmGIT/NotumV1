#!/bin/bash

# This script automates the setup and execution of the ChatGPT scraper.
# It ensures a virtual environment is used and all dependencies are installed.

# --- Configuration ---
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
SCRIPT_FILE="scraper.py"

# --- Functions ---
function print_info {
    echo "--- $1 ---"
}

function print_error {
    echo "ERREUR: $1" >&2
    exit 1
}

# --- Main Execution ---

# 1. Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 n'est pas installé. Veuillez l'installer pour continuer."
fi

# 2. Set up Virtual Environment
if [ ! -d "$VENV_DIR" ]; then
    print_info "Création de l'environnement virtuel dans le dossier '$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        print_error "Échec de la création de l'environnement virtuel."
    fi
fi

# 3. Activate Virtual Environment
print_info "Activation de l'environnement virtuel..."
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    print_error "Échec de l'activation de l'environnement virtuel."
fi

# 4. Install/Update Dependencies
print_info "Installation des dépendances depuis '$REQUIREMENTS_FILE'..."
pip install -r "$REQUIREMENTS_FILE"
if [ $? -ne 0 ]; then
    print_error "Échec de l'installation des dépendances."
fi

# 5. Install Playwright browsers
print_info "Installation des navigateurs pour Playwright (cela peut prendre un moment)..."
playwright install --with-deps
if [ $? -ne 0 ]; then
    print_error "Échec de l'installation des navigateurs Playwright."
fi

# 6. Run the Scraper
print_info "Lancement du script de scraping..."
python3 "$SCRIPT_FILE"
if [ $? -ne 0 ]; then
    print_error "Le script de scraping s'est terminé avec une erreur."
fi

print_info "Le script a terminé son exécution."

# Deactivate the virtual environment upon completion
deactivate

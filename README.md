# Notum - Collecteur de Données ChatGPT

Ce projet contient un outil pour télécharger une copie de toutes vos conversations depuis votre compte ChatGPT.

## Comment l'utiliser

L'utilisation est conçue pour être aussi simple que possible.

### Prérequis

- Vous devez être sur un système d'exploitation Linux (comme Ubuntu).
- Vous devez avoir `git` et `python3` installés.

### Instructions

1.  **Clonez le projet (si ce n'est pas déjà fait)**
    Ouvrez un terminal et clonez ce projet sur votre ordinateur.
    ```bash
    git clone <URL_DU_PROJET>
    cd <NOM_DU_DOSSIER_DU_PROJET>
    ```

2.  **Exécutez le lanceur**
    Dans le terminal, à l'intérieur du dossier du projet, lancez la commande suivante :
    ```bash
    ./lancer_le_scraper.sh
    ```
    Vous pouvez aussi souvent double-cliquer sur le fichier `lancer_le_scraper.sh` depuis votre explorateur de fichiers.

### Première utilisation

- La première fois que vous lancez le script, il installera tout ce qui est nécessaire (cela peut prendre quelques minutes).
- Une fenêtre de navigateur s'ouvrira. Vous devrez vous y connecter à votre compte ChatGPT.
- Une fois connecté, revenez au terminal et appuyez sur la touche `Entrée`.
- La session de connexion sera sauvegardée dans un fichier `session.json`.

### Utilisations suivantes

- Lancez simplement `./lancer_le_scraper.sh` à nouveau.
- Le script utilisera la session sauvegardée pour se connecter automatiquement et commencera à télécharger vos conversations.

## Où sont sauvegardées les données ?

Les conversations seront sauvegardées dans un dossier `data/` qui sera créé automatiquement. Le fichier s'appellera `chatgpt_conversations.jsonl`.

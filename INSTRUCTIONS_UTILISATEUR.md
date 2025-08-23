# Instructions pour Activer le Scraper ChatGPT

Bonjour ! Voici le guide complet pour lancer le scraper et récupérer vos conversations ChatGPT. Suivez ces étapes dans l'ordre.

## Prérequis

-   Vous avez `git` et `python3` installés sur votre machine Ubuntu.
-   Vous avez cloné le projet depuis GitHub.

## Étape 1 : Mettre à jour le code

Assurez-vous d'avoir la dernière version du code. Ouvrez un terminal dans le dossier du projet (`NotumV1`) et lancez :

```bash
# Annule les modifications locales pour éviter les conflits
git checkout -- .

# Télécharge la dernière version
git pull
```

## Étape 2 : Créer et Activer l'Environnement Virtuel

C'est une "bulle" pour notre projet. **Cette étape n'est à faire qu'une seule fois.** Si le dossier `venv` existe déjà, vous n'avez pas besoin de la recréer.

```bash
# Créer l'environnement (s'il n'existe pas déjà)
python3 -m venv venv

# Activer l'environnement (à faire chaque fois que vous ouvrez un nouveau terminal)
source venv/bin/activate
```
Votre invite de commande devrait maintenant commencer par `(venv)`.

## Étape 3 : Installer les Dépendances

Installez les bibliothèques Python nécessaires (Playwright, etc.) dans notre environnement virtuel.

```bash
pip install -r requirements.txt
```

## Étape 4 : Lancer le Scraper (Authentification)

C'est ici que vous lancez le script. La première fois, il vous demandera de vous connecter.

```bash
python3 chatgpt.py
```

**Que va-t-il se passer ?**
1.  Le script va afficher un message et **ouvrir une fenêtre de navigateur**.
2.  Dans cette fenêtre, **connectez-vous à votre compte ChatGPT** comme vous le faites d'habitude. Passez les éventuels CAPTCHAs.
3.  Une fois que vous êtes bien connecté et que vous voyez l'interface principale de ChatGPT, **revenez à votre terminal**.
4.  Appuyez sur la touche **`Entrée`** dans le terminal.

Le script va alors sauvegarder votre session de connexion dans un fichier `session.json` et la fenêtre du navigateur se fermera.

## Étape 5 : Lancer le Scraper (Collecte des données)

Relancez **exactement la même commande** :

```bash
python3 chatgpt.py
```

Cette fois, le script verra que le fichier `session.json` existe. Il ne vous demandera pas de vous connecter. Il va directement :
1.  Se connecter en arrière-plan (headless).
2.  Parcourir toutes vos conversations une par une.
3.  Sauvegarder leur contenu dans le fichier `chatgpt_conversations.jsonl`.

Cela peut prendre plusieurs minutes si vous avez beaucoup de conversations.

---

Une fois ces étapes terminées, le fichier `chatgpt_conversations.jsonl` contiendra toutes vos données, prêt pour la prochaine phase du projet !

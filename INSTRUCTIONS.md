# Instructions Finales pour le Scraper Notum

Bonjour,

Voici le guide **définitif et simplifié** pour lancer le scraper et récupérer vos conversations ChatGPT. Le projet a été nettoyé pour rendre ces étapes aussi simples que possible.

### Étape 1 : Récupérer la dernière version du projet

Si vous avez déjà le projet, le plus simple est de forcer une mise à jour pour être sûr d'avoir la version propre. Ouvrez un terminal dans le dossier `NotumV1`.

```bash
# 1. Récupère les dernières informations de GitHub
git fetch --all

# 2. Force la mise à jour de votre dossier local vers la branche stable
git reset --hard origin/version-stable-scraper
```

Si vous n'avez pas le projet, clonez-le et basculez sur la bonne branche :
```bash
git clone [URL_DE_VOTRE_DEPOT]
cd NotumV1
git checkout version-stable-scraper
```

### Étape 2 : Préparer l'environnement (une seule fois)

Toujours depuis le dossier `NotumV1` :

```bash
# 1. Créez un environnement virtuel nommé 'venv'
python3 -m venv venv

# 2. Activez-le
source venv/bin/activate

# 3. Installez les dépendances
pip install -r requirements.txt
```
Après l'activation, vous verrez `(venv)` au début de votre ligne de commande.

### Étape 3 : Lancer le Scraper

C'est la commande que vous utiliserez à chaque fois. Assurez-vous que votre environnement est activé (que `(venv)` est visible).

```bash
python3 chatgpt.py
```

**La première fois uniquement :**
- Un navigateur s'ouvrira.
- Connectez-vous à ChatGPT.
- Revenez au terminal et appuyez sur `Entrée`.

**Toutes les fois suivantes :**
- Le script se lancera directement, sans navigateur visible, et commencera à collecter les données.

Les conversations seront sauvegardées dans `chatgpt_conversations.jsonl`.

C'est tout ! Le projet est maintenant beaucoup plus simple à utiliser.

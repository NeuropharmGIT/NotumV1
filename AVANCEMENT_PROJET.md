# Suivi de l'avancement du projet Notum

Ce document suit les étapes de développement du projet. Il sera mis à jour à chaque nouvelle fonctionnalité.

## Statut Actuel

**Phase 1 : Collecte de Données - TERMINÉE**

## Étapes Réalisées

-   **[✓] 2025-08-22 : Initialisation et Débogage**
    -   Premières tentatives de mise en place et nombreux problèmes de configuration.
-   **[✓] 2025-08-22 : Réinitialisation du Projet**
    -   Le projet a été réinitialisé à un état propre pour résoudre les problèmes de structure.
-   **[✓] 2025-08-22 : Implémentation du Scraper ChatGPT**
    -   Création d'un script autonome (`chatgpt.py`) pour la collecte de données via scraping.
    -   Gestion de l'authentification manuelle et utilisation de `playwright-stealth` pour la discrétion.
    -   Sauvegarde des conversations extraites dans `chatgpt_conversations.jsonl`.
-   **[✓] 2025-08-22 : Création des Fichiers de Suivi**
    -   Mise en place de ce fichier d'avancement.
    -   Mise en place du fichier de méthodologie de projet (`METHODOLOGIE_PROJET.md`).

## Prochaines Étapes Prévues (Feuille de Route)

-   **[ ] Phase 2 : Ingestion et Structuration des Données**
    -   Lire le fichier `chatgpt_conversations.jsonl`.
    -   Mettre en place une base de données locale (SQLite).
    -   Créer un schéma de base de données (tables pour messages, conversations, etc.).
    -   Écrire un script pour "ingérer" les données JSONL dans la base de données SQLite.
    -   Gérer la déduplication pour ne pas insérer plusieurs fois les mêmes messages.

-   **[ ] Phase 3 : Analyse et Concordeur Narratif**
    -   Mettre en place l'indexation pour la recherche en texte intégral (SQLite FTS5).
    -   Mettre en place une base de données vectorielle (par ex. Qdrant) pour la recherche sémantique.
    -   Développer la logique pour détecter les liens et contradictions.

-   **[ ] Phase 4 : Débat Multi-Agents**
    -   Intégrer des modèles de langage locaux (LLM).
    -   Mettre en place le framework pour le débat (par ex. LangGraph ou AutoGen).
    -   Développer la logique pour le "débat A/B" et la génération d'accords.

-   **[ ] Phase 5 : Interface Utilisateur**
    -   Créer une interface simple (par ex. en ligne de commande ou avec une bibliothèque comme Gradio/Streamlit) pour interagir avec le système.

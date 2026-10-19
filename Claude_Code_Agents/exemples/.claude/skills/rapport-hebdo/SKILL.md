---
name: rapport-hebdo
description: Rédige le rapport d'activité hebdomadaire de l'équipe à partir de l'historique Git. À utiliser quand l'utilisateur demande un rapport, un bilan ou un résumé de la semaine.
---

# Rapport hebdomadaire

1. Exécute `scripts/collecter.sh` pour obtenir les commits des 7 derniers jours, groupés par auteur.
2. Classe les changements en : Fonctionnalités, Corrections, Technique, Documentation.
3. Remplis le modèle `modele.md` (même dossier) sans en changer la structure.
4. Reste factuel : n'invente aucune information absente de l'historique.

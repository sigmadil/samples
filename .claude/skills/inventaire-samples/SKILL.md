---
name: inventaire-samples
description: Produit un inventaire des exemples BHoM du dépôt, par toolkit et par format (.dyn, .gh, .xlsx…). À utiliser quand on demande la liste, le nombre ou un tableau récapitulatif des exemples.
---

# Inventaire des exemples

1. Exécute le script fourni depuis la racine du dépôt :

   ```bash
   python3 .claude/skills/inventaire-samples/inventaire.py
   ```

   Il affiche un tableau Markdown : une ligne par toolkit, une colonne par extension.

2. Présente le tableau tel quel, puis ajoute 2 ou 3 observations utiles, par exemple
   le toolkit le plus fourni, ou les toolkits qui n'ont des exemples que pour un
   seul logiciel (Dynamo ou Grasshopper).

3. Si l'utilisateur demande un toolkit précis, passe son nom en argument :

   ```bash
   python3 .claude/skills/inventaire-samples/inventaire.py Revit_Toolkit
   ```

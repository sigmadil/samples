"""Inventaire des exemples BHoM : nombre de fichiers par toolkit et par extension."""
import sys
from collections import Counter, defaultdict
from pathlib import Path

IGNORES = {".git", ".claude", "Formation_Agents_IA"}

racine = Path(__file__).resolve().parents[3]
cibles = sys.argv[1:] or sorted(
    p.name for p in racine.iterdir() if p.is_dir() and p.name not in IGNORES
)

compteurs = defaultdict(Counter)
for toolkit in cibles:
    for fichier in (racine / toolkit).rglob("*"):
        if fichier.is_file():
            compteurs[toolkit][fichier.suffix.lower() or "(sans)"] += 1

extensions = sorted({ext for c in compteurs.values() for ext in c})
print("| Toolkit | " + " | ".join(extensions) + " | Total |")
print("|---" * (len(extensions) + 2) + "|")
for toolkit in cibles:
    c = compteurs[toolkit]
    cellules = [str(c.get(ext, "")) for ext in extensions]
    print(f"| {toolkit} | " + " | ".join(cellules) + f" | {sum(c.values())} |")

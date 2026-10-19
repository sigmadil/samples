#!/usr/bin/env bash
# Hook PreToolUse : bloque les commandes Bash destructrices.
# Reçoit le JSON de l'appel d'outil sur stdin ; le code de sortie 2 bloque l'appel
# et renvoie le message de stderr à Claude.
set -euo pipefail
commande=$(jq -r '.tool_input.command // empty')

if grep -Eq '(rm -rf|git push --force|git reset --hard|DROP TABLE)' <<<"$commande"; then
  echo "Commande bloquée par la politique du projet : $commande" >&2
  exit 2
fi
exit 0

#!/usr/bin/env bash
# Liste les commits des 7 derniers jours, groupés par auteur.
set -euo pipefail
git log --since="7 days ago" --no-merges --pretty=format:'%an|%h|%s' \
  | sort \
  | awk -F'|' '$1 != auteur { auteur = $1; print "\n## " auteur } { print "- " $2 " " $3 }'

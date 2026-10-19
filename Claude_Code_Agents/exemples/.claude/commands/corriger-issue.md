---
description: Analyse et corrige une issue GitHub à partir de son numéro
argument-hint: <numéro-issue>
allowed-tools: Bash(gh issue view:*), Bash(git:*), Read, Edit, Grep, Glob
---

Corrige l'issue GitHub n°$1.

Contexte de l'issue :
!`gh issue view $1`

Étapes :
1. Reformule le problème en une phrase.
2. Localise le code concerné.
3. Écris d'abord un test qui reproduit le problème.
4. Corrige le code, puis lance les tests.
5. Propose un message de commit au format Conventional Commits.

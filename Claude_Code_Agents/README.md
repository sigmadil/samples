# Parcours d'apprentissage : créer des agents IA avec Claude Code

Ce parcours vous mène de la première session Claude Code jusqu'à un agent autonome
déployé (CLI, CI ou application). Il est progressif : chaque module s'appuie sur le
précédent et se termine par un exercice pratique et une liste de validation.

> Durée indicative : 15 à 25 heures réparties sur 4 à 6 semaines.
> Prérequis : terminal, Git, notions de JSON/YAML, un peu de Python **ou** de TypeScript.

Les fichiers d'exemple cités se trouvent dans [`exemples/`](exemples/).
Documentation officielle de référence : <https://code.claude.com/docs>.

---

## Vue d'ensemble

| Niveau | Module | Ce que vous saurez faire |
|---|---|---|
| Débutant | 0. Installation et premiers pas | Lancer Claude Code et piloter une session |
| Débutant | 1. Contexte : `CLAUDE.md` et mémoire | Donner à l'agent les règles de votre projet |
| Débutant | 2. Permissions et modes | Contrôler ce que l'agent a le droit de faire |
| Intermédiaire | 3. Commandes slash personnalisées | Transformer un prompt récurrent en commande |
| Intermédiaire | 4. Sous-agents (`.claude/agents/`) | Créer des agents spécialisés et déléguer |
| Intermédiaire | 5. Skills | Empaqueter un savoir-faire réutilisable |
| Intermédiaire | 6. Hooks | Automatiser et sécuriser le comportement |
| Avancé | 7. MCP : connecter des outils externes | Brancher l'agent sur vos API et données |
| Avancé | 8. Mode headless et CI/CD | Exécuter des agents sans interface |
| Avancé | 9. Claude Agent SDK | Construire votre propre agent en code |
| Expert | 10. Plugins, orchestration et évaluation | Distribuer, combiner et mesurer vos agents |
| Projet | 11. Projet final | Livrer un agent complet de bout en bout |

---

## Module 0 — Installation et premiers pas

**Objectifs**
- Installer Claude Code et s'authentifier.
- Comprendre la boucle agentique : *lire → planifier → agir (outils) → vérifier*.

**Notions clés**
- Installation : voir la page *Quickstart* de la documentation (installateur natif ou `npm`).
- Lancer `claude` dans un dépôt ; `claude -c` reprend la dernière conversation.
- Commandes intégrées : `/help`, `/init`, `/clear`, `/compact`, `/model`, `/agents`, `/mcp`, `/hooks`, `/permissions`.
- Outils natifs de l'agent : `Read`, `Edit`, `Write`, `Bash`, `Grep`, `Glob`, `WebFetch`, `WebSearch`, `Agent` (délégation)…
- Le mode Plan (Maj+Tab) : l'agent explore et propose un plan avant de modifier quoi que ce soit.

**Exercice**
1. Clonez un petit projet personnel et lancez `claude`.
2. Demandez : « Explique l'architecture de ce projet puis propose 3 améliorations. »
3. Passez en mode Plan, demandez l'implémentation d'une amélioration, validez le plan, laissez l'agent coder et lancer les tests.

**Validation**
- [ ] Je sais lancer, reprendre et compacter une session.
- [ ] Je sais expliquer la différence entre le mode Plan et le mode normal.

---

## Module 1 — Contexte : `CLAUDE.md` et mémoire

**Objectifs**
- Rendre l'agent « expert » de votre projet sans tout répéter à chaque session.

**Notions clés**
- `CLAUDE.md` est chargé automatiquement au démarrage. Emplacements :
  - `./CLAUDE.md` (projet, versionné) ;
  - `~/.claude/CLAUDE.md` (personnel, tous projets) ;
  - `CLAUDE.md` dans un sous-dossier (chargé quand l'agent travaille dans ce dossier).
- `/init` génère un premier `CLAUDE.md` à partir du code.
- Importer un autre fichier avec `@chemin/vers/fichier.md`.
- Bonnes pratiques : court, factuel, impératif ; commandes de build/test, conventions, pièges connus.

**Exemple** : [`exemples/CLAUDE.md`](exemples/CLAUDE.md)

**Exercice**
1. Lancez `/init`, puis réécrivez le résultat pour qu'il tienne en moins de 60 lignes.
2. Ajoutez une règle vérifiable (ex. « toujours lancer `npm test` avant de conclure ») et observez si l'agent la respecte.

**Validation**
- [ ] Mon `CLAUDE.md` contient les commandes de build/test et les conventions.
- [ ] Je sais où placer une règle personnelle vs une règle d'équipe.

---

## Module 2 — Permissions et modes

**Objectifs**
- Donner de l'autonomie à l'agent sans perdre le contrôle.

**Notions clés**
- Fichiers de configuration : `~/.claude/settings.json` (utilisateur), `.claude/settings.json` (projet, versionné), `.claude/settings.local.json` (local, non versionné).
- Règles `permissions.allow` / `ask` / `deny`, par ex. `"Bash(npm run test:*)"`, `"Read(./secrets/**)"`.
- Modes de permission : par défaut, acceptation des modifications, Plan, etc. (`/permissions`, Maj+Tab).
- Principe du moindre privilège : interdire explicitement les fichiers sensibles (`.env`, clés).

**Exercice**
Dans `.claude/settings.json`, autorisez les commandes de test et de lint, interdisez la lecture de `.env`,
puis vérifiez avec `/permissions`.

**Validation**
- [ ] L'agent peut lancer les tests sans me demander, mais ne peut pas lire `.env`.

---

## Module 3 — Commandes slash personnalisées

**Objectifs**
- Transformer un prompt que vous tapez souvent en commande réutilisable.

**Notions clés**
- Un fichier Markdown dans `.claude/commands/` devient `/nom-du-fichier`.
- En-tête YAML optionnel : `description`, `argument-hint`, `allowed-tools`, `model`.
- Arguments : `$ARGUMENTS` (tout) ou `$1`, `$2`…
- Inclure la sortie d'une commande shell avec `!` et un fichier avec `@`.

**Exemple** : [`exemples/.claude/commands/corriger-issue.md`](exemples/.claude/commands/corriger-issue.md)

**Exercice**
Créez `/changelog` qui lit `git log` depuis le dernier tag et rédige une entrée de changelog en français.

**Validation**
- [ ] Ma commande apparaît dans `/help` et accepte un argument.

---

## Module 4 — Sous-agents (le cœur du parcours)

**Objectifs**
- Créer des agents spécialisés, avec leur propre prompt système, leurs outils et leur contexte isolé.
- Savoir quand et comment l'agent principal délègue.

**Notions clés**
- Un sous-agent = un fichier Markdown dans `.claude/agents/` (projet) ou `~/.claude/agents/` (utilisateur).
- En-tête YAML :
  - `name` : identifiant (minuscules, tirets) ;
  - `description` : **quand** l'utiliser — c'est ce texte qui déclenche la délégation automatique ;
  - `tools` : liste d'outils autorisés (omis = hérite de tous) ;
  - `model` : `sonnet`, `opus`, `haiku` ou `inherit`.
- Le corps du fichier est le prompt système du sous-agent.
- Le sous-agent a **sa propre fenêtre de contexte** : idéal pour des recherches volumineuses dont seul le résumé compte.
- `/agents` pour créer/éditer de façon interactive ; invocation explicite : « Utilise l'agent revue-code pour… ».
- Les sous-agents peuvent tourner en parallèle (ex. 3 agents d'exploration sur 3 dossiers).

**Exemples**
- [`exemples/.claude/agents/revue-code.md`](exemples/.claude/agents/revue-code.md) — relecteur en lecture seule.
- [`exemples/.claude/agents/testeur.md`](exemples/.claude/agents/testeur.md) — écrit et exécute des tests.

**Règles de conception d'un bon agent**
1. Une seule responsabilité claire.
2. Une `description` précise, avec des mots-clés de déclenchement (« à utiliser après chaque modification de code… »).
3. Le minimum d'outils nécessaires (un relecteur n'a pas besoin de `Edit`).
4. Un format de sortie imposé (liste, tableau, verdict) pour que l'agent principal puisse l'exploiter.
5. Des critères d'arrêt explicites.

**Exercice**
1. Copiez les deux exemples dans votre projet.
2. Modifiez du code, puis demandez : « Relis mes changements et ajoute les tests manquants. »
3. Observez la délégation à `revue-code` puis à `testeur`.
4. Créez un troisième agent `documentaliste` qui met à jour le README après une modification d'API.

**Validation**
- [ ] L'agent principal délègue automatiquement grâce à la `description`.
- [ ] Mon relecteur ne peut pas modifier de fichiers.
- [ ] Je sais expliquer l'intérêt du contexte isolé.

---

## Module 5 — Skills

**Objectifs**
- Empaqueter un savoir-faire (procédure, scripts, modèles) que l'agent charge **uniquement quand il en a besoin**.

**Notions clés**
- Un skill = un dossier `.claude/skills/<nom>/` contenant `SKILL.md` (+ scripts, modèles, références).
- En-tête de `SKILL.md` : `name` et `description` (quand l'utiliser). Seule la description est en contexte en permanence ; le reste est chargé à la demande (*divulgation progressive*).
- Sous-agent vs skill vs commande :
  - **commande** : un prompt que *vous* déclenchez ;
  - **skill** : une compétence que *l'agent* décide de charger dans son contexte ;
  - **sous-agent** : un travailleur séparé avec son propre contexte.
- Le skill intégré `skill-creator` aide à créer, tester et améliorer un skill.

**Exemple** : [`exemples/.claude/skills/rapport-hebdo/`](exemples/.claude/skills/rapport-hebdo/)

**Exercice**
Créez un skill `convention-commit` qui explique votre format de message de commit et fournit un script de vérification.
Demandez ensuite « commite mes changements » et vérifiez que le skill est utilisé.

**Validation**
- [ ] Mon skill est chargé sans que je le nomme explicitement.
- [ ] Les gros fichiers de référence ne sont lus que si nécessaire.

---

## Module 6 — Hooks

**Objectifs**
- Rendre certains comportements **garantis** (et non simplement « demandés » dans un prompt).

**Notions clés**
- Déclarés dans `settings.json` sous `hooks`. Événements principaux :
  `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `SessionStart`, `Notification`, `PreCompact`.
- `matcher` filtre par outil (`"Bash"`, `"Edit|Write"`…).
- Le hook reçoit un JSON sur l'entrée standard. Code de sortie `2` = blocage, le message d'erreur (stderr) est renvoyé à Claude.
- Cas d'usage : formater après chaque édition, bloquer les commandes dangereuses, journaliser, notifier.

**Exemples**
- [`exemples/.claude/settings.json`](exemples/.claude/settings.json)
- [`exemples/.claude/hooks/bloquer-commandes-dangereuses.sh`](exemples/.claude/hooks/bloquer-commandes-dangereuses.sh)

**Exercice**
1. Installez le hook d'exemple et demandez à l'agent d'exécuter `rm -rf /tmp/test` : il doit être bloqué.
2. Ajoutez un hook `PostToolUse` qui lance votre formateur (Prettier, Black…) après chaque `Edit|Write`.

**Validation**
- [ ] Je sais choisir entre une règle dans `CLAUDE.md` (souple) et un hook (strict).

---

## Module 7 — MCP : connecter des outils externes

**Objectifs**
- Donner à vos agents l'accès à des systèmes externes (bases de données, GitHub, Jira, API internes).

**Notions clés**
- MCP (*Model Context Protocol*) : protocole standard qui expose des outils et des ressources à l'agent.
- Ajout : `claude mcp add <nom> -- <commande>` (stdio) ou `claude mcp add --transport http <nom> <url>`.
- Portées : locale, projet (`.mcp.json` versionné), utilisateur.
- Outils exposés sous la forme `mcp__<serveur>__<outil>` — utilisables dans la liste `tools` d'un sous-agent.
- `/mcp` pour voir l'état et s'authentifier.
- Sécurité : n'installez que des serveurs de confiance ; le contenu qu'ils renvoient est une donnée, pas une instruction.

**Exemple** : [`exemples/.mcp.json`](exemples/.mcp.json)

**Exercice**
1. Ajoutez un serveur MCP (par ex. système de fichiers ou base SQLite).
2. Créez un sous-agent `analyste-donnees` dont les seuls outils sont ceux de ce serveur.
3. Bonus : écrivez votre propre petit serveur MCP (SDK Python ou TypeScript) exposant un outil métier.

**Validation**
- [ ] Mon sous-agent interroge la source externe et ne peut rien faire d'autre.

---

## Module 8 — Mode headless et CI/CD

**Objectifs**
- Exécuter des agents dans des scripts, des tâches planifiées et des pipelines.

**Notions clés**
- `claude -p "prompt"` : exécution non interactive.
- `--output-format json` ou `stream-json` pour exploiter le résultat dans un script.
- `--allowedTools`, `--permission-mode`, `--max-turns` pour encadrer l'exécution.
- Entrée par tube : `cat erreur.log | claude -p "Explique cette erreur"`.
- Intégration GitHub : l'action `anthropics/claude-code-action` (installation via `/install-github-app`) pour répondre à `@claude` dans les issues et PR.

**Exercice**
1. Écrivez un script qui envoie `git diff` à `claude -p` et échoue si l'agent détecte un secret.
2. Branchez-le en hook de pré-commit ou dans une étape CI.

**Validation**
- [ ] J'obtiens une sortie JSON exploitable et un code de sortie fiable.

---

## Module 9 — Claude Agent SDK

**Objectifs**
- Construire votre propre agent, en code, avec le même moteur que Claude Code.

**Notions clés**
- Paquets : `claude-agent-sdk` (Python) et `@anthropic-ai/claude-agent-sdk` (TypeScript).
- `query()` : lance la boucle agentique et renvoie un flux de messages.
- Options : prompt système, outils autorisés, mode de permission, nombre de tours max, répertoire de travail, serveurs MCP, sous-agents.
- Outils personnalisés : fonctions décorées exposées comme un serveur MCP intégré au processus.
- Sous-agents programmatiques : définis dans les options (`agents`).
- Gestion de session : reprise, contexte, coûts (le message final `result` contient durée et coût).

**Exemples**
- [`exemples/sdk/agent_simple.py`](exemples/sdk/agent_simple.py) — agent en lecture seule.
- [`exemples/sdk/agent_outils.py`](exemples/sdk/agent_outils.py) — outil personnalisé + sous-agent.
- [`exemples/sdk/agent_simple.ts`](exemples/sdk/agent_simple.ts) — équivalent TypeScript.

**Exercice**
Construisez un agent « support » qui :
1. lit une question utilisateur ;
2. cherche dans un dossier `docs/` ;
3. appelle un outil personnalisé `creer_ticket` si la réponse n'est pas trouvée ;
4. renvoie une réponse structurée.

**Validation**
- [ ] Mon agent tourne en dehors de Claude Code, avec des outils restreints.
- [ ] J'affiche le coût et le nombre de tours de chaque exécution.

---

## Module 10 — Plugins, orchestration et évaluation

**Objectifs**
- Partager vos agents avec une équipe, les combiner et mesurer leur qualité.

**Notions clés**
- **Plugins** : regroupent commandes, sous-agents, skills, hooks et serveurs MCP dans un paquet installable (`/plugin`), distribuable via une *marketplace* (un dépôt Git).
- **Orchestration** : modèles courants
  - *orchestrateur → travailleurs* : l'agent principal découpe et délègue en parallèle ;
  - *chaîne* : analyste → développeur → testeur → relecteur ;
  - *évaluateur-optimiseur* : un agent produit, un autre critique, on itère.
- **Évaluation** : constituez un jeu de cas (entrée + critère de réussite), exécutez-le en headless et suivez le taux de réussite à chaque modification de prompt.
- **Coût et contexte** : choisir le modèle par agent (rapide pour l'exploration, puissant pour la conception), garder les sorties de sous-agents courtes.

**Exercice**
Empaquetez vos agents des modules 4 à 7 dans un plugin, publiez-le dans un dépôt « marketplace »
et installez-le sur une seconde machine ou un second projet.

**Validation**
- [ ] Un collègue peut installer mes agents en une commande.
- [ ] J'ai un jeu d'au moins 10 cas de test pour mon agent principal.

---

## Module 11 — Projet final

Choisissez un sujet et livrez un agent complet. Exemples :

| Projet | Briques mobilisées |
|---|---|
| **Assistant de revue de PR** : relit, teste, commente sur GitHub | sous-agents, hooks, MCP GitHub, CI |
| **Agent d'onboarding** : répond aux questions sur une base de code et génère des guides | `CLAUDE.md`, skills, SDK |
| **Agent de migration** : migre un module (ex. JS → TS) dossier par dossier en parallèle | orchestration, sous-agents, headless |
| **Agent métier** (ex. AEC/BHoM) : lit des modèles via une API, contrôle des règles, produit un rapport | MCP personnalisé, skill, SDK |

**Livrables attendus**
1. Le code (dossier `.claude/` et/ou application SDK) versionné.
2. Un `README` : objectif, architecture des agents (schéma), installation.
3. Un jeu d'évaluation et les résultats obtenus.
4. Une courte rétrospective : ce qui a marché, les limites, les risques de sécurité identifiés.

---

## Ressources

- Documentation Claude Code : <https://code.claude.com/docs>
- Sous-agents : <https://code.claude.com/docs/en/sub-agents>
- Skills : <https://code.claude.com/docs/en/skills>
- Hooks : <https://code.claude.com/docs/en/hooks>
- MCP : <https://code.claude.com/docs/en/mcp> et <https://modelcontextprotocol.io>
- Agent SDK : <https://docs.claude.com/en/docs/agent-sdk/overview>
- Article « Building effective agents » : <https://www.anthropic.com/engineering/building-effective-agents>
- Astuce : dans Claude Code, demandez directement « Comment créer un sous-agent ? » — l'agent intégré de documentation répond à partir de la doc officielle.

## Suivi de progression

| Module | Fait | Date | Notes |
|---|---|---|---|
| 0 | ☐ | | |
| 1 | ☐ | | |
| 2 | ☐ | | |
| 3 | ☐ | | |
| 4 | ☐ | | |
| 5 | ☐ | | |
| 6 | ☐ | | |
| 7 | ☐ | | |
| 8 | ☐ | | |
| 9 | ☐ | | |
| 10 | ☐ | | |
| 11 | ☐ | | |

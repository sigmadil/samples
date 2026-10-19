# Formation : créer des agents IA avec Claude Code

Parcours pratique, du plus simple au plus avancé. Chaque module contient un exemple
**fonctionnel dans ce dépôt** (exemples BHoM Dynamo / Grasshopper / Excel), pour
apprendre en manipulant de vrais fichiers.

| Module | Sujet | Fichiers d'exemple |
|---|---|---|
| 1 | Les notions : agent, sous-agent, skill, hook, MCP | — |
| 2 | Créer son premier sous-agent | `.claude/agents/dyn-analyzer.md` |
| 3 | Restreindre les outils et choisir le modèle | `.claude/agents/samples-reviewer.md` |
| 4 | Les skills (savoir-faire réutilisable) | `.claude/skills/inventaire-samples/SKILL.md` |
| 5 | Orchestrer plusieurs agents | — |
| 6 | Sortir de Claude Code : le Claude Agent SDK | `Formation_Agents_IA/sdk/agent_sdk_exemple.py` |
| 7 | Exercices | — |

---

## Module 1 : les notions de base

Un **agent**, c'est un modèle de langage qui tourne en boucle : il lit la demande,
choisit un outil (lire un fichier, lancer une commande…), observe le résultat, puis
recommence jusqu'à ce que la tâche soit terminée. Claude Code est lui-même un agent.

Dans Claude Code, plusieurs briques permettent de le spécialiser :

| Brique | Ce que c'est | Où ça se trouve |
|---|---|---|
| **Sous-agent** (subagent) | Un assistant spécialisé, avec son propre prompt système, ses propres outils et **son propre contexte**. Claude lui délègue une tâche et ne reçoit que son rapport final. | `.claude/agents/<nom>.md` (projet) ou `~/.claude/agents/<nom>.md` (utilisateur) |
| **Skill** | Des instructions (et éventuellement des scripts) que Claude charge **dans son propre contexte** quand la tâche s'y prête. | `.claude/skills/<nom>/SKILL.md` |
| **Slash command** | Un prompt réutilisable lancé avec `/nom`. | `.claude/commands/<nom>.md` |
| **Hook** | Une commande shell exécutée automatiquement sur un événement (avant/après un outil, fin de session…). | `.claude/settings.json` |
| **Serveur MCP** | Un connecteur qui ajoute des outils externes (GitHub, base de données, API…). | `.mcp.json` ou `claude mcp add` |
| **CLAUDE.md** | La mémoire du projet : conventions, commandes, contexte. Lu à chaque session. | Racine du projet |

**Sous-agent ou skill ?**
- Sous-agent : la tâche produit beaucoup de bruit (lecture de dizaines de fichiers,
  logs…) et vous ne voulez que la conclusion. Le contexte principal reste propre.
- Skill : vous voulez apprendre un savoir-faire à Claude lui-même, qu'il applique
  directement dans la conversation.

---

## Module 2 : créer son premier sous-agent

Un sous-agent est un simple fichier Markdown avec un en-tête YAML.

```markdown
---
name: dyn-analyzer
description: Analyse un script Dynamo (.dyn) BHoM et en explique le fonctionnement. À utiliser dès qu'on demande ce que fait un fichier .dyn.
tools: Read, Glob, Grep, Bash
model: sonnet
---

Tu es un expert Dynamo et BHoM. Quand on te donne un fichier .dyn :
1. ...
```

| Champ | Rôle |
|---|---|
| `name` | Identifiant unique, en minuscules avec tirets. |
| `description` | **Le champ le plus important.** Claude s'en sert pour décider *quand* déléguer. Décrivez le « quand », pas seulement le « quoi ». Ajouter « à utiliser de manière proactive » encourage la délégation automatique. |
| `tools` | Liste des outils autorisés. Si absent, l'agent hérite de tous les outils de la session. |
| `model` | `sonnet`, `opus`, `haiku` ou `inherit` (même modèle que la session). |
| Corps du fichier | Le prompt système de l'agent. |

### Deux façons de créer un agent

1. **Interactive** : tapez `/agents` dans Claude Code → *Create new agent* →
   choisissez projet ou utilisateur → laissez Claude générer un brouillon, puis
   ajustez-le.
2. **Manuelle** : créez le fichier `.claude/agents/<nom>.md` vous-même.

### À essayer dans ce dépôt

L'agent [`dyn-analyzer`](../.claude/agents/dyn-analyzer.md) est déjà prêt. Lancez
`claude` à la racine du dépôt, puis :

```
> Que fait le script Revit_Toolkit/Dynamo/Pull/PullSelection.dyn ?
```

Claude devrait déléguer automatiquement à `dyn-analyzer` grâce à sa description.
Pour forcer l'appel :

```
> Utilise l'agent dyn-analyzer pour expliquer Revit_Toolkit/Dynamo/Push/PushElements.dyn
```

Vous pouvez aussi mentionner l'agent directement avec `@` (tapez `@dyn` et
choisissez-le dans la liste).

---

## Module 3 : restreindre les outils et choisir le modèle

Bonne pratique : **donner à chaque agent le minimum d'outils nécessaires.**

- Un agent de relecture n'a pas besoin de `Edit` ni de `Write`. Sans ces outils,
  il ne peut rien casser.
- `Bash` est puissant : ne le donnez que si l'agent doit vraiment exécuter des
  commandes.
- Les outils MCP s'écrivent `mcp__<serveur>__<outil>` (exemple :
  `mcp__github__list_issues`).

Choix du modèle :

| Modèle | Quand l'utiliser |
|---|---|
| `haiku` | Tâches simples, rapides et répétitives (inventaires, extraction). Le moins cher. |
| `sonnet` | Le bon compromis pour la plupart des agents. |
| `opus` | Raisonnement difficile : architecture, revue approfondie. |
| `inherit` | Reprend le modèle de la session principale. |

Exemple : [`samples-reviewer`](../.claude/agents/samples-reviewer.md) est un relecteur
en **lecture seule** (`Read, Glob, Grep`) qui vérifie la cohérence des exemples
(versions BHoM mélangées, doublons `_ver01`/`_ver02`, fichiers sans équivalent
Dynamo/Grasshopper…).

```
> Demande à samples-reviewer de vérifier le dossier TAS_Toolkit
```

---

## Module 4 : les skills

Une skill est un dossier contenant un `SKILL.md` :

```
.claude/skills/inventaire-samples/
├── SKILL.md          # instructions + en-tête name/description
└── inventaire.py     # script optionnel que la skill fait exécuter
```

```markdown
---
name: inventaire-samples
description: Produit un inventaire des exemples BHoM du dépôt (par toolkit et par format). À utiliser quand on demande la liste, le nombre ou un tableau des exemples.
---

Lance `python3 .claude/skills/inventaire-samples/inventaire.py` puis présente ...
```

Claude ne lit au départ que le `name` et la `description` de chaque skill. Il ne charge
le corps que lorsqu'elle est utile, ce qui permet d'en avoir beaucoup sans saturer
le contexte. Vous pouvez aussi l'appeler explicitement avec `/inventaire-samples`.

À essayer :

```
> Fais-moi un inventaire des exemples du dépôt
```

---

## Module 5 : orchestrer plusieurs agents

Quelques schémas courants :

1. **Délégation simple** : l'agent principal confie une sous-tâche à un spécialiste
   et reçoit le résultat.
2. **En parallèle** : plusieurs sous-agents travaillent en même temps sur des parties
   indépendantes.
   ```
   > En parallèle, utilise dyn-analyzer sur chaque fichier de Revit_Toolkit/Dynamo/Pull
     et fais-moi un tableau récapitulatif
   ```
3. **Chaîne** : la sortie d'un agent alimente le suivant.
   ```
   > Utilise samples-reviewer pour trouver les problèmes dans Excel_Toolkit,
     puis dyn-analyzer pour détailler les .dyn qu'il signale
   ```

Règles d'or :
- Un sous-agent **ne voit pas** la conversation principale : son prompt (la tâche
  que Claude lui transmet) doit contenir tout le contexte utile.
- Demandez-lui un **format de sortie précis** (tableau, liste, verdict). Seul son
  rapport final revient dans le contexte principal.
- Un agent = une responsabilité. Mieux vaut trois petits agents clairs qu'un seul
  agent fourre-tout.

---

## Module 6 : le Claude Agent SDK

Le SDK permet d'utiliser le moteur de Claude Code **dans vos propres programmes**
(Python ou TypeScript) : scripts d'automatisation, intégration continue, applications.

```bash
pip install claude-agent-sdk
export ANTHROPIC_API_KEY=...   # clé API depuis console.anthropic.com
python Formation_Agents_IA/sdk/agent_sdk_exemple.py
```

Le fichier [`sdk/agent_sdk_exemple.py`](sdk/agent_sdk_exemple.py) montre :
- `query()` : lancer un agent et parcourir ses messages ;
- `ClaudeAgentOptions` : outils autorisés, prompt système, mode de permission ;
- `AgentDefinition` : déclarer des sous-agents directement dans le code.

Documentation : https://docs.claude.com/en/docs/agent-sdk/overview

---

## Module 7 : exercices

1. **Lire** : ouvrez `.claude/agents/dyn-analyzer.md`, changez `model: sonnet` en
   `model: haiku`, relancez la même question et comparez les résultats.
2. **Créer** : avec `/agents`, créez un agent `gh-inventory` qui liste les fichiers
   Grasshopper (`.gh`) n'ayant pas d'équivalent `.dyn` du même nom.
   Indice : il suffit de `Glob` et d'un bon prompt.
3. **Restreindre** : retirez `Bash` de `dyn-analyzer`. L'agent fonctionne-t-il
   encore ? Comment contourne-t-il le problème ?
4. **Skill** : créez une skill `nouveau-sample` qui explique comment ajouter un
   exemple dans le dépôt (dossier, nommage, versions Dynamo et Grasshopper).
5. **SDK** : modifiez `agent_sdk_exemple.py` pour écrire le rapport dans un fichier
   Markdown au lieu de l'afficher.

### Checklist d'un bon agent

- [ ] La `description` dit **quand** l'utiliser, avec des mots que l'utilisateur
      emploierait réellement.
- [ ] Le prompt définit un rôle, une méthode étape par étape et un format de sortie.
- [ ] Les outils sont réduits au strict nécessaire.
- [ ] Le modèle est adapté à la difficulté de la tâche.
- [ ] Le fichier est versionné dans `.claude/agents/` pour être partagé avec l'équipe.

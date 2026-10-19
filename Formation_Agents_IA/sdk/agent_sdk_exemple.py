"""Exemple Claude Agent SDK : un agent qui audite les scripts Dynamo du dépôt.

Installation :
    pip install claude-agent-sdk
    export ANTHROPIC_API_KEY=...

Lancement, depuis la racine du dépôt :
    python Formation_Agents_IA/sdk/agent_sdk_exemple.py
"""
import asyncio

from claude_agent_sdk import (
    AgentDefinition,
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)

# Sous-agent déclaré dans le code : équivalent d'un fichier .claude/agents/*.md
analyseur_dyn = AgentDefinition(
    description="Explique ce que fait un script Dynamo (.dyn) BHoM.",
    prompt=(
        "Tu es un expert Dynamo/BHoM. Un .dyn est du JSON (clés Nodes, Connectors). "
        "Extrais les ConcreteType des nœuds avec Python plutôt que de lire tout le "
        "fichier, puis résume en 3 lignes : objectif, adapter utilisé, entrées."
    ),
    tools=["Read", "Bash"],
    model="haiku",
)

options = ClaudeAgentOptions(
    system_prompt="Tu es un assistant qui documente les exemples BHoM. Réponds en français.",
    # Outils autorisés pour l'agent principal ("Agent" lui permet de déléguer).
    allowed_tools=["Read", "Glob", "Grep", "Bash", "Agent"],
    agents={"dyn-analyzer": analyseur_dyn},
    # Lecture seule dans cet exemple : on refuse toute modification de fichier.
    disallowed_tools=["Edit", "Write"],
    max_turns=30,
)

PROMPT = (
    "Liste les fichiers .dyn de Revit_Toolkit/Dynamo/Pull. Pour chacun, délègue "
    "l'analyse au sous-agent dyn-analyzer, puis rends un tableau Markdown "
    "(fichier | objectif | adapter)."
)


async def main():
    async for message in query(prompt=PROMPT, options=options):
        if isinstance(message, AssistantMessage):
            for bloc in message.content:
                if isinstance(bloc, TextBlock):
                    print(bloc.text)
        elif isinstance(message, ResultMessage):
            print(f"\n--- Terminé en {message.num_turns} tours, coût : {message.total_cost_usd} $")


if __name__ == "__main__":
    asyncio.run(main())

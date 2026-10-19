"""Agent avec un outil personnalisé et un sous-agent, via le Claude Agent SDK.

Installation : pip install claude-agent-sdk
"""
import asyncio
from typing import Any

from claude_agent_sdk import (
    AgentDefinition,
    ClaudeAgentOptions,
    ResultMessage,
    create_sdk_mcp_server,
    query,
    tool,
)


@tool("creer_ticket", "Crée un ticket de support quand la documentation ne répond pas", {"titre": str, "detail": str})
async def creer_ticket(args: dict[str, Any]) -> dict[str, Any]:
    # Remplacez par un appel à votre outil de ticketing (Jira, GitHub Issues…).
    print(f"[ticket] {args['titre']} — {args['detail']}")
    return {"content": [{"type": "text", "text": "Ticket SUP-42 créé."}]}


support = create_sdk_mcp_server(name="support", version="1.0.0", tools=[creer_ticket])


async def main() -> None:
    options = ClaudeAgentOptions(
        system_prompt=(
            "Tu es l'agent de support. Cherche d'abord la réponse dans docs/ via l'agent chercheur-docs. "
            "Si elle est introuvable, crée un ticket avec l'outil creer_ticket."
        ),
        mcp_servers={"support": support},
        allowed_tools=["Read", "Grep", "Glob", "Agent", "mcp__support__creer_ticket"],
        agents={
            "chercheur-docs": AgentDefinition(
                description="Cherche une réponse dans le dossier docs/ et renvoie un extrait cité.",
                prompt="Cherche dans docs/ uniquement. Renvoie l'extrait pertinent avec fichier:ligne, ou 'INTROUVABLE'.",
                tools=["Read", "Grep", "Glob"],
                model="haiku",
            )
        },
        max_turns=15,
    )

    async for message in query(prompt="Comment réinitialiser mon mot de passe ?", options=options):
        if isinstance(message, ResultMessage):
            print(message.result)


if __name__ == "__main__":
    asyncio.run(main())

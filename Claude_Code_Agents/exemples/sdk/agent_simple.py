"""Agent minimal en lecture seule avec le Claude Agent SDK.

Installation : pip install claude-agent-sdk
Exécution    : python agent_simple.py "Quels fichiers gèrent l'authentification ?"
"""
import asyncio
import sys

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, query


async def main(question: str) -> None:
    options = ClaudeAgentOptions(
        system_prompt="Tu es un guide de base de code. Réponds en français, en citant fichier:ligne.",
        allowed_tools=["Read", "Grep", "Glob"],
        max_turns=10,
    )

    async for message in query(prompt=question, options=options):
        if isinstance(message, AssistantMessage):
            for bloc in message.content:
                if isinstance(bloc, TextBlock):
                    print(bloc.text)
        elif isinstance(message, ResultMessage):
            print(f"\n--- {message.num_turns} tours, coût : {message.total_cost_usd} USD")


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "Résume ce projet."))

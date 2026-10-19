// Agent minimal en lecture seule avec le Claude Agent SDK (TypeScript).
// Installation : npm install @anthropic-ai/claude-agent-sdk
// Exécution    : npx tsx agent_simple.ts "Quels fichiers gèrent l'authentification ?"
import { query } from "@anthropic-ai/claude-agent-sdk";

const question = process.argv.slice(2).join(" ") || "Résume ce projet.";

for await (const message of query({
  prompt: question,
  options: {
    systemPrompt: "Tu es un guide de base de code. Réponds en français, en citant fichier:ligne.",
    allowedTools: ["Read", "Grep", "Glob"],
    maxTurns: 10,
  },
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
    console.log(`--- ${message.num_turns} tours, coût : ${message.total_cost_usd} USD`);
  }
}

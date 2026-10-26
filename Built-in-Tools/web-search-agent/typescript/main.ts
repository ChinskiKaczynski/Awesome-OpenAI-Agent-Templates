/**
 * Web Search Agent
 * Real-time internet search using the web_search built-in tool.
 */
import OpenAI from "openai";
import { validateWebSearchResponse, type SearchResult } from "./validation.ts";

const openai = new OpenAI();

async function searchWeb(query: string): Promise<SearchResult> {
    console.log(`🔍 Query: ${query}`);
    console.log("🌐 Searching the web...");

    const response = await openai.responses.create({
        model: "gpt-4.1-mini",
        input: query,
        tools: [{ type: "web_search" }],
        tool_choice: "required",
    });

    return validateWebSearchResponse(response);
}

async function main() {
    const queries = [
        "Who is the current president of France?",
        "What are the latest developments in AI?",
    ];

    for (const query of queries) {
        const { answer, sources } = await searchWeb(query);
        console.log(`🤖 Answer: ${answer}\n`);
        console.log("Sources:\n" + sources.map(url => `- ${url}`).join("\n"));
        console.log("-".repeat(50) + "\n");
    }
}

main().catch(error => {
    console.error("Web search failed:", error);
    process.exitCode = 1;
});

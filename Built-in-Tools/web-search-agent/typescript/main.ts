/**
 * Web Search Agent
 * Real-time internet search using the web_search built-in tool.
 */
import OpenAI from "openai";

const openai = new OpenAI();

async function searchWeb(query: string): Promise<string> {
    console.log(`🔍 Query: ${query}`);
    console.log("🌐 Searching the web...");

    const response = await openai.responses.create({
        model: "gpt-4o-mini",
        input: query,
        tools: [{ type: "web_search_preview" }],
    });

    return response.output_text;
}

async function main() {
    const queries = [
        "Who is the current president of France?",
        "What are the latest developments in AI?",
    ];

    for (const query of queries) {
        const answer = await searchWeb(query);
        console.log(`🤖 Answer: ${answer}\n`);
        console.log("-".repeat(50) + "\n");
    }
}

main();

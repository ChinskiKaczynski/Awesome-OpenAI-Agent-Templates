/**
 * Responses API - Minimal Starter
 * The simplest possible example using OpenAI's Responses API.
 */
import OpenAI from "openai";

const openai = new OpenAI();

async function main() {
    const response = await openai.responses.create({
        model: "gpt-4o-mini",
        input: "Hello! Tell me about yourself in one sentence.",
    });

    console.log(`🤖 Response: ${response.output_text}`);
    console.log(response.usage ? `📊 Usage: ${response.usage.total_tokens} tokens` : "📊 Usage: unavailable");
}

main();

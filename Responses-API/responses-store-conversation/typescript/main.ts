/**
 * Responses API - Stateful Conversations
 * Multi-turn conversations with store=true and previous_response_id.
 */
import { existsSync } from "node:fs";
import { loadEnvFile } from "node:process";
import OpenAI from "openai";

// Load the optional .env file before the SDK reads OPENAI_API_KEY.
if (existsSync(".env")) {
    loadEnvFile(".env");
}

const openai = new OpenAI();

async function main() {
    // First message - start the conversation
    console.log("👤 User: Tell me a joke");

    const response = await openai.responses.create({
        model: "gpt-4o-mini",
        input: "Tell me a joke",
        store: true, // Persist response on OpenAI servers
    });

    console.log(`🤖 Assistant: ${response.output_text}\n`);

    // Second message - chain with previous_response_id
    console.log("👤 User: Explain why it's funny");

    const secondResponse = await openai.responses.create({
        model: "gpt-4o-mini",
        previous_response_id: response.id, // Chain to previous
        input: [{ role: "user", content: "Explain why this is funny." }],
        store: true,
    });

    console.log(`🤖 Assistant: ${secondResponse.output_text}\n`);

    // Third message - continue the chain
    console.log("👤 User: Give me another joke on a similar theme");

    const thirdResponse = await openai.responses.create({
        model: "gpt-4o-mini",
        previous_response_id: secondResponse.id,
        input: [{ role: "user", content: "Give me another joke on a similar theme." }],
        store: true,
    });

    console.log(`🤖 Assistant: ${thirdResponse.output_text}`);

    // Print conversation chain info
    console.log(`\n📊 Conversation chain:`);
    console.log(`   Response 1 ID: ${response.id}`);
    console.log(`   Response 2 ID: ${secondResponse.id}`);
    console.log(`   Response 3 ID: ${thirdResponse.id}`);
}

main();

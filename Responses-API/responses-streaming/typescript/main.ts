/**
 * Responses API - Streaming
 * Real-time streaming responses using Server-Sent Events (SSE).
 */
import OpenAI from "openai";

const openai = new OpenAI();

async function main() {
    console.log("🔄 Streaming response...\n");

    const stream = await openai.responses.create({
        model: "gpt-4o-mini",
        input: [
            {
                role: "user",
                content: "Explain quantum entanglement in simple terms.",
            },
        ],
        stream: true,
    });

    for await (const event of stream) {
        // Handle text delta events
        if (event.type === "response.output_text.delta") {
            process.stdout.write(event.delta);
        }

        // Handle completion
        if (event.type === "response.completed") {
            console.log(`\n\n✅ Complete! Total tokens: ${event.response.usage?.total_tokens}`);
        }
    }
}

main();

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

    let completed = false;
    for await (const event of stream) {
        if (event.type === "response.output_text.delta") {
            process.stdout.write(event.delta);
        } else if (event.type === "response.completed") {
            completed = true;
            const tokens = event.response.usage?.total_tokens;
            console.log(tokens == null
                ? "\n\n✅ Complete! Token usage unavailable."
                : `\n\n✅ Complete! Total tokens: ${tokens}`);
        } else if (event.type === "response.failed") {
            throw new Error(`Response failed: ${event.response.error?.message ?? "Unknown error"}`);
        } else if (event.type === "response.incomplete") {
            throw new Error(`Response incomplete: ${event.response.incomplete_details?.reason ?? "Unknown reason"}`);
        }
    }
    if (!completed) {
        throw new Error("Response stream ended without a completion event.");
    }
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});

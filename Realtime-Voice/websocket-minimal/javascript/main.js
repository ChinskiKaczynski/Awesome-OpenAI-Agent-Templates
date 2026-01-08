/**
 * Realtime API - WebSocket Minimal (GA)
 * Basic WebSocket connection to the Realtime API using gpt-realtime model.
 * 
 * Run: node main.js
 */
import WebSocket from "ws";
import dotenv from "dotenv";

dotenv.config();

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const MODEL = "gpt-realtime"; // GA model (replaces gpt-4o-realtime-preview)

const url = `wss://api.openai.com/v1/realtime?model=${MODEL}`;

console.log("🔌 Connecting to Realtime API...");
console.log(`   Model: ${MODEL}`);
console.log(`   URL: ${url.slice(0, 50)}...\n`);

const ws = new WebSocket(url, {
    headers: {
        Authorization: `Bearer ${OPENAI_API_KEY}`,
    },
});

ws.on("open", function open() {
    console.log("✅ Connected to Realtime API!");

    // GA requires explicit session type configuration
    const sessionConfig = {
        type: "session.update",
        session: {
            type: "realtime", // REQUIRED in GA (not needed in beta)
            instructions: "You are a friendly voice assistant. Respond concisely.",
            voice: "alloy", // Options: alloy, cedar, marin, etc.
            input_audio_format: "pcm16",
            output_audio_format: "pcm16",
        },
    };

    ws.send(JSON.stringify(sessionConfig));
    console.log("⚙️  Session configured");
    console.log("🎤 Ready for audio input (this demo shows connection only)");
});

ws.on("message", function incoming(message) {
    const data = JSON.parse(message.toString());
    const eventType = data.type || "unknown";

    switch (eventType) {
        case "session.created":
            console.log(`📡 Session created: ${data.session?.id || "unknown"}`);
            break;

        case "session.updated":
            console.log("✅ Session updated successfully");
            break;

        case "response.audio.delta":
            // In a real app, you'd play this audio
            console.log("🔊 Received audio chunk");
            break;

        case "response.done":
            console.log("✅ Response complete");
            break;

        case "error":
            console.log(`❌ Error: ${data.error?.message || "Unknown error"}`);
            break;

        default:
            console.log(`📨 Event: ${eventType}`);
    }
});

ws.on("error", function error(err) {
    console.log(`❌ WebSocket error: ${err.message}`);
});

ws.on("close", function close(code, reason) {
    console.log(`🔌 Connection closed: ${code} - ${reason}`);
});

// Keep the process alive for demo
// In production, this would be managed differently
setTimeout(() => {
    console.log("\n⏱️  Demo timeout - closing connection");
    ws.close();
    process.exit(0);
}, 10000);

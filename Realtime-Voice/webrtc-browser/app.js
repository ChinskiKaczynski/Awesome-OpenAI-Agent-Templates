/**
 * Realtime Voice Agent - WebRTC
 * Browser-based voice agent using WebRTC for lowest latency.
 * 
 * ⚠️ DEMO ONLY: In production, use ephemeral tokens from your backend.
 */

// Configuration
const MODEL = "gpt-realtime";
const INSTRUCTIONS = "You are a friendly voice assistant. Be helpful and concise.";

// State
let peerConnection = null;
let dataChannel = null;
let audioStream = null;

// DOM Elements
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const statusEl = document.getElementById("status");
const transcriptEl = document.getElementById("transcript");

// Event handlers
startBtn.addEventListener("click", startSession);
stopBtn.addEventListener("click", stopSession);

/**
 * Start the voice session
 */
async function startSession() {
    try {
        updateStatus("Requesting microphone access...", "connecting");

        // Get microphone access
        audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });

        updateStatus("Connecting to Realtime API...", "connecting");

        // Create peer connection
        peerConnection = new RTCPeerConnection();

        // Add audio track
        audioStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, audioStream);
        });

        // Create data channel for events
        dataChannel = peerConnection.createDataChannel("oai-events");
        dataChannel.onopen = () => {
            console.log("Data channel open");
            sendSessionConfig();
        };
        dataChannel.onmessage = handleMessage;

        // Handle incoming audio
        peerConnection.ontrack = (event) => {
            const audioEl = document.createElement("audio");
            audioEl.srcObject = event.streams[0];
            audioEl.autoplay = true;
            document.body.appendChild(audioEl);
        };

        // Create offer
        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);

        // In a real app, you would:
        // 1. Send this offer to your backend
        // 2. Backend exchanges it with OpenAI using ephemeral token
        // 3. Backend returns the answer

        // For demo purposes, show instructions
        updateStatus("⚠️ Demo: See console for WebRTC setup instructions", "warning");
        console.log("WebRTC Offer created. In production:");
        console.log("1. Send this offer to your backend");
        console.log("2. Backend uses ephemeral token to get answer from OpenAI");
        console.log("3. Set remote description with the answer");
        console.log("\nOffer SDP:", offer.sdp);

        addToTranscript("system", "WebRTC connection demo started. See console for implementation details.");

        // Update UI
        startBtn.disabled = true;
        stopBtn.disabled = false;

    } catch (error) {
        console.error("Error starting session:", error);
        updateStatus(`Error: ${error.message}`, "error");
    }
}

/**
 * Stop the voice session
 */
function stopSession() {
    if (audioStream) {
        audioStream.getTracks().forEach(track => track.stop());
        audioStream = null;
    }

    if (dataChannel) {
        dataChannel.close();
        dataChannel = null;
    }

    if (peerConnection) {
        peerConnection.close();
        peerConnection = null;
    }

    updateStatus("Disconnected", "ready");
    startBtn.disabled = false;
    stopBtn.disabled = true;

    addToTranscript("system", "Session ended.");
}

/**
 * Send session configuration via data channel
 */
function sendSessionConfig() {
    if (dataChannel && dataChannel.readyState === "open") {
        const config = {
            type: "session.update",
            session: {
                type: "realtime",
                instructions: INSTRUCTIONS,
                voice: "alloy",
            }
        };
        dataChannel.send(JSON.stringify(config));
        console.log("Session config sent");
    }
}

/**
 * Handle incoming messages from data channel
 */
function handleMessage(event) {
    try {
        const data = JSON.parse(event.data);
        console.log("Received:", data.type);

        switch (data.type) {
            case "response.audio_transcript.delta":
                // Update transcript with AI response
                addToTranscript("assistant", data.delta);
                break;

            case "input_audio_buffer.speech_started":
                addToTranscript("user", "[Speaking...]");
                break;

            case "error":
                console.error("API Error:", data.error);
                updateStatus(`Error: ${data.error?.message}`, "error");
                break;
        }
    } catch (e) {
        console.error("Error parsing message:", e);
    }
}

/**
 * Update status display
 */
function updateStatus(text, state = "ready") {
    statusEl.textContent = text;
    statusEl.className = `status ${state}`;
}

/**
 * Add message to transcript
 */
function addToTranscript(role, text) {
    // Remove placeholder if present
    const placeholder = transcriptEl.querySelector(".placeholder");
    if (placeholder) {
        placeholder.remove();
    }

    const p = document.createElement("p");
    p.className = role;

    const label = document.createElement("strong");
    label.textContent = role === "user" ? "You: " :
        role === "assistant" ? "AI: " : "System: ";

    p.appendChild(label);
    p.appendChild(document.createTextNode(text));
    transcriptEl.appendChild(p);

    // Scroll to bottom
    transcriptEl.scrollTop = transcriptEl.scrollHeight;
}

# Realtime WebSocket Minimal

Minimal WebSocket voice agent using the Realtime API GA.

## Python

```bash
cd python
pip install websocket-client python-dotenv
python main.py
```

## JavaScript (Node.js)

```bash
cd javascript
npm install
node main.js
```

## What it does

1. Connects to `wss://api.openai.com/v1/realtime?model=gpt-realtime`
2. Configures session with `type: "realtime"`
3. Listens for events from the API
4. Ready to send/receive audio data

## Key Events

| Event | Direction | Description |
|-------|-----------|-------------|
| `session.created` | Server → Client | Connection established |
| `session.update` | Client → Server | Configure session |
| `input_audio_buffer.append` | Client → Server | Send audio data |
| `response.audio.delta` | Server → Client | Receive audio chunk |

## GA vs Beta

```javascript
// Beta (deprecated - sunset Feb 27, 2026)
// No session type required

// GA (current)
session: {
    type: "realtime",  // REQUIRED
    instructions: "..."
}
```

## Expected Output

```
🔌 Connecting to Realtime API...
✅ Connected!
📡 Session created: sess_abc123
⚙️  Configuring session...
🎤 Ready for audio input
```

## Next Steps

- Add microphone input → see advanced examples
- Add speaker output for responses
- Integrate with frontend → [webrtc-browser](../webrtc-browser/)

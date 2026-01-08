# Realtime Voice Templates

Templates for building **voice-enabled AI agents** using the OpenAI Realtime API GA.

> 📚 **Official Docs**: [Realtime API Guide](https://platform.openai.com/docs/guides/realtime)

## ⚠️ Deprecation Notice

| Old API/Model | Deprecation Date | Replacement |
|---------------|------------------|-------------|
| Realtime API Beta | Feb 27, 2026 | Realtime API GA |
| gpt-4o-realtime-preview | Mar 24, 2026 | gpt-realtime |

**Action Required**: Migrate to GA API and `gpt-realtime` model.

## Available Templates

| Template | Connection | Platform | Description |
|----------|------------|----------|-------------|
| [websocket-minimal](./websocket-minimal/) | WebSocket | Server | Basic voice agent with WebSocket |
| [webrtc-browser](./webrtc-browser/) | WebRTC | Browser | Client-side voice in browser |

## Connection Types

| Type | Best For | Latency |
|------|----------|---------|
| **WebSocket** | Server-side apps, Node.js, Python | Low |
| **WebRTC** | Browser apps, client-side | Very low |
| **SIP** | Telephony integration | Varies |

## GA API Changes

The GA Realtime API includes breaking changes from Beta:

```javascript
// GA requires explicit session type
ws.send(JSON.stringify({
    type: "session.update",
    session: {
        type: "realtime",  // NEW: required in GA
        instructions: "Be helpful"
    }
}));
```

## Quick Start

### WebSocket (Python)

```bash
cd websocket-minimal/python
pip install websocket-client python-dotenv
python main.py
```

### WebRTC (Browser)

```bash
cd webrtc-browser
# Open index.html in browser
```

## Model Comparison

| Model | Status | Features |
|-------|--------|----------|
| `gpt-realtime` | ✅ GA | Full featured, 20% cheaper |
| `gpt-4o-realtime-preview` | ⚠️ Deprecated | Sunset Mar 2026 |

## External Resources

- 🔗 [OpenAI Realtime Agents Demo](https://github.com/openai/openai-realtime-agents)
- 🔗 [WebRTC Documentation](https://platform.openai.com/docs/guides/realtime-webrtc)

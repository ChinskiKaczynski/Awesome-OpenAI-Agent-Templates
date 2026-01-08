# Realtime WebRTC Browser

Browser-based voice agent using WebRTC for lowest latency.

## Usage

1. Create `.env` with your API key
2. Open `index.html` in browser (or serve with local server)
3. Click "Start" to begin voice interaction

> ⚠️ **Security Note**: In production, use ephemeral tokens instead of exposing API keys in the browser.

## What it does

1. Requests microphone access
2. Establishes WebRTC connection to Realtime API
3. Streams audio bidirectionally in real-time
4. Displays transcript of conversation

## Why WebRTC over WebSocket?

| Feature | WebRTC | WebSocket |
|---------|--------|-----------|
| Latency | Very low | Low |
| Browser support | ✅ Native | ✅ Native |
| NAT traversal | ✅ Built-in | ❌ Requires setup |
| Audio handling | ✅ Native | Manual encoding |

## Files

| File | Description |
|------|-------------|
| `index.html` | Main HTML page |
| `app.js` | WebRTC logic |
| `style.css` | Styling |

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 80+
- ✅ Safari 15+
- ✅ Edge 90+

## Expected Flow

```
1. User clicks "Start"
2. Browser requests microphone access
3. WebRTC connection established
4. User speaks → Audio sent to API
5. API responds → Audio plays in browser
6. Transcript appears on screen
```

## For Production

Replace API key with ephemeral tokens:

```javascript
// Get ephemeral token from your backend
const response = await fetch('/api/get-realtime-token');
const { token } = await response.json();

// Use token for WebRTC connection
```

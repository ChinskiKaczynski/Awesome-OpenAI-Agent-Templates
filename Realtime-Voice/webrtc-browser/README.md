# Realtime WebRTC Browser

**Status: signaling scaffold, not a working voice agent.** The browser code creates
a WebRTC SDP offer but does not exchange it with OpenAI or apply a remote SDP
answer. Opening the page alone cannot establish a voice session or show a live
transcript.

## Inspect the scaffold

1. Serve this directory on localhost (microphone access requires a secure context):

   ```bash
   python -m http.server 8000
   ```

2. Open `http://localhost:8000` and click **Start**.
3. Allow microphone access and inspect the SDP offer in the browser console.
   Click **Stop** to release the microphone and close the local peer connection.

There is no backend in this directory. The page does not read a `.env` file,
use an API key, or make a request to the Realtime API.

## What is missing for a real conversation

- Add a trusted backend to exchange the browser's SDP offer for an answer
  through the Realtime WebRTC API (or mint an ephemeral client secret).
  Keep the standard OpenAI API key on the backend, never in browser code.
- Send the offer, receive the SDP answer, and call
  `peerConnection.setRemoteDescription(...)` in `app.js`.
- Update the session configuration and transcript event handler in `app.js`
  to the current Realtime GA schema before connecting. The existing
  top-level `session.voice` and `response.audio_transcript.delta` are outdated.

See the [official OpenAI WebRTC guide](https://developers.openai.com/api/docs/guides/voice-webrtc?voice-api=realtime)
for a complete connection flow.

## Files

| File | Description |
|------|-------------|
| `index.html` | Browser UI |
| `app.js` | Microphone, peer connection, SDP offer, and event scaffold |
| `style.css` | Styling |

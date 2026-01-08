"""
Realtime API - WebSocket Minimal (GA)
Basic WebSocket connection to the Realtime API using gpt-realtime model.

Requirements:
    pip install websocket-client python-dotenv
"""
import os
import json
import websocket
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-realtime"  # GA model (replaces gpt-4o-realtime-preview)

URL = f"wss://api.openai.com/v1/realtime?model={MODEL}"
HEADERS = ["Authorization: Bearer " + OPENAI_API_KEY]


def on_open(ws):
    """Called when WebSocket connection is established."""
    print("✅ Connected to Realtime API!")
    
    # GA requires explicit session type configuration
    session_config = {
        "type": "session.update",
        "session": {
            "type": "realtime",  # REQUIRED in GA (not needed in beta)
            "instructions": "You are a friendly voice assistant. Respond concisely.",
            "voice": "alloy",  # Options: alloy, cedar, marin, etc.
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
        }
    }
    
    ws.send(json.dumps(session_config))
    print("⚙️  Session configured")
    print("🎤 Ready for audio input (this demo shows connection only)")


def on_message(ws, message):
    """Handle incoming messages from the API."""
    data = json.loads(message)
    event_type = data.get("type", "unknown")
    
    if event_type == "session.created":
        session_id = data.get("session", {}).get("id", "unknown")
        print(f"📡 Session created: {session_id}")
    
    elif event_type == "session.updated":
        print("✅ Session updated successfully")
    
    elif event_type == "response.audio.delta":
        # In a real app, you'd play this audio
        print("🔊 Received audio chunk")
    
    elif event_type == "response.done":
        print("✅ Response complete")
    
    elif event_type == "error":
        error = data.get("error", {})
        print(f"❌ Error: {error.get('message', 'Unknown error')}")
    
    else:
        # Log other events for debugging
        print(f"📨 Event: {event_type}")


def on_error(ws, error):
    """Handle WebSocket errors."""
    print(f"❌ WebSocket error: {error}")


def on_close(ws, close_status_code, close_msg):
    """Handle WebSocket close."""
    print(f"🔌 Connection closed: {close_status_code} - {close_msg}")


def main():
    print("🔌 Connecting to Realtime API...")
    print(f"   Model: {MODEL}")
    print(f"   URL: {URL[:50]}...\n")
    
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not set")
        return
    
    ws = websocket.WebSocketApp(
        URL,
        header=HEADERS,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    
    # Run for a short time to demonstrate connection
    # In production, this would run indefinitely
    ws.run_forever()


if __name__ == "__main__":
    main()

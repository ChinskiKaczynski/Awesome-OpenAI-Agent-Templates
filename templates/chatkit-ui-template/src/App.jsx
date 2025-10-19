import React, { useState } from 'react'

export default function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const send = async () => {
    if (!input.trim()) return
    const userMsg = { role: 'user', content: input }
    setMessages(m => [...m, userMsg])
    setInput('')
    const res = await fetch('http://localhost:8787/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMsg.content }),
    })
    const data = await res.json()
    setMessages(m => [...m, { role: 'assistant', content: data.reply }])
  }
  return (
    <div style={{ maxWidth: 720, margin: '40px auto', fontFamily: 'system-ui' }}>
      <h1>Chat UI (proxy → OpenAI)</h1>
      <div style={{ border: '1px solid #ddd', padding: 16, borderRadius: 12, minHeight: 240 }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: 8 }}>
            <strong>{m.role === 'user' ? 'Ty' : 'Agent'}:</strong> {m.content}
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Napisz wiadomość…"
          style={{ flex: 1, padding: 8, borderRadius: 8, border: '1px solid #ccc' }}
        />
        <button onClick={send} style={{ padding: '8px 16px', borderRadius: 8 }}>Wyślij</button>
      </div>
    </div>
  )
}

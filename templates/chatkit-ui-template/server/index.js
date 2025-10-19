import 'dotenv/config'
import express from 'express'
import cors from 'cors'
import { OpenAI } from 'openai'

const app = express()
app.use(cors())
app.use(express.json())

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
const PORT = process.env.PORT || 8787

app.post('/api/chat', async (req, res) => {
  try {
    const message = String(req.body?.message || '')
    const completion = await client.chat.completions.create({
      model: 'gpt-4.1-mini',
      messages: [
        { role: 'system', content: 'You are a helpful assistant. Keep answers brief.' },
        { role: 'user', content: message }
      ]
    })
    res.json({ reply: completion.choices[0].message.content })
  } catch (e) {
    console.error(e)
    res.status(500).json({ error: 'Server error' })
  }
})

app.listen(PORT, () => console.log(`Server on http://localhost:${PORT}`))

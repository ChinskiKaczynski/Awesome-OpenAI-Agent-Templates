# Deploying the ChatKit UI on Vercel

**Goal:** Deploy the Next.js ChatKit template with a secure session endpoint.

## Prerequisites
- Vercel account
- Next.js app
- `OPENAI_API_KEY`

## Steps
1. **Fork/Copy** the ChatKit template files.
2. **Set Env Vars** in Vercel Project Settings:
   - `OPENAI_API_KEY`
   - `NEXT_PUBLIC_WORKFLOW_ID` (your Agent Builder workflow ID)
3. **Routes**
   - `/api/chatkit/start` creates a session by POSTing to `https://api.openai.com/v1/chatkit/sessions` with `OpenAI-Beta: chatkit_beta=v1`.
4. **Build & Deploy**
   - `npm i && npm run build`, then deploy.
5. **Verify**
   - Open the deployed URL; the widget should initialize via server-provided `client_secret`.

## Hardening
- Rotate tokens and implement `/api/chatkit/refresh` for long chats.
- Restrict origins (CORS) to your domains.
- Log request IDs and handle 4xx/5xx gracefully.

## References
- ChatKit sessions/auth guides and example starter repos.

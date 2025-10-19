# ChatKit UI Template (Hosted Integration)

**Goal:** Embed **ChatKit** in your app and connect it to an **Agent Builder** workflow via a short-lived client token.

> ChatKit hosted flow requires creating a **session** on your server and returning a short-lived `client_secret` to the browser. Clients never see your API key.

## Project structure (Next.js example)
```
/app
  /api
    /chatkit
      start/route.ts     # create session
      refresh/route.ts   # refresh token
  page.tsx               # renders ChatKit
.env
```

## Server: create a session
**`app/api/chatkit/start/route.ts`**
```ts
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const { userId, workflowId } = await req.json();

    const r = await fetch("https://api.openai.com/v1/chatkit/sessions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "OpenAI-Beta": "chatkit_beta=v1",
        "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        workflow: { id: workflowId }, // e.g. wf_...
        user: userId || "anonymous",
        // optional: chatkit_configuration: { file_upload: { enabled: true } }
      }),
    });

    if (!r.ok) {
      const err = await r.text();
      return NextResponse.json({ error: err }, { status: r.status });
    }

    const data = await r.json();
    // Expecting { client_secret, expires_at, ... }
    return NextResponse.json({ client_secret: data.client_secret });
  } catch (e: any) {
    return NextResponse.json({ error: e?.message || "unknown error" }, { status: 500 });
  }
}
```

**`app/api/chatkit/refresh/route.ts`** (optional)
```ts
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  // In production, repeat session creation or call a refresh endpoint when available,
  // then return a new client_secret before expiration.
  return NextResponse.json({ error: "Not implemented" }, { status: 501 });
}
```

## Client: render ChatKit
**`app/page.tsx`**
```tsx
"use client";

import { useEffect, useRef } from "react";

export default function Home() {
  const ref = useRef<any>(null);

  useEffect(() => {
    // Load ChatKit script (if not added globally)
    const s = document.createElement("script");
    s.src = "https://cdn.platform.openai.com/deployments/chatkit/chatkit.js";
    s.async = true;
    s.onload = init;
    document.head.appendChild(s);

    async function init() {
      async function getClientSecret() {
        const res = await fetch("/api/chatkit/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            userId: "demo-user-123",
            workflowId: process.env.NEXT_PUBLIC_WORKFLOW_ID, // set in .env
          }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "session error");
        return data.client_secret;
      }

      // @ts-ignore - web component provided by the script
      const el = document.createElement("openai-chatkit");
      el.style.height = "600px";
      el.style.width = "100%";
      el.theme = "light";
      el.getClientSecret = getClientSecret; // required
      ref.current?.appendChild(el);
    }
  }, []);

  return <div className="container" ref={ref} />;
}
```

## Env
```bash
OPENAI_API_KEY=sk-...
NEXT_PUBLIC_WORKFLOW_ID=wf_...
```

## Run
```bash
npm i
npm run dev
```

## Notes
- Uses **/v1/chatkit/sessions** with `OpenAI-Beta: chatkit_beta=v1` to obtain `client_secret`.
- For file uploads and custom config, initialize with `chatkit_configuration` in your server request (when supported).
- See official ChatKit docs and auth flow.

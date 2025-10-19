"use client";

import { useEffect, useRef } from "react";

export default function Home() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const s = document.createElement("script");
    s.src = "https://cdn.platform.openai.com/deployments/chatkit/chatkit.js";
    s.async = true;
    s.onload = init;
    document.head.appendChild(s);

    async function init() {
      async function getClientSecret(existing?: { client_secret: string, expires_at: string }) {
        if (existing) {
          // Here you could call /api/chatkit/refresh
        }
        const res = await fetch("/api/chatkit/start", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            userId: "demo-user-123",
            workflowId: process.env.NEXT_PUBLIC_WORKFLOW_ID,
          }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "session error");
        return data.client_secret;
      }

      // @ts-ignore - web component provided by ChatKit script
      const el = document.createElement("openai-chatkit");
      el.style.height = "600px";
      el.style.width = "100%";
      el.theme = "light";
      el.getClientSecret = getClientSecret;
      ref.current?.appendChild(el);
    }
  }, []);

  return <div className="container" ref={ref} />;
}

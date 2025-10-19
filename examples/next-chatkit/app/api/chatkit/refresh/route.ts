import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";

export async function POST(req: NextRequest) {
  try {
    const { userId, workflowId } = await req.json();
    const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    const session = await client.chatkit.sessions.create({
      workflow: { id: workflowId },
      user: userId || "anonymous",
    });
    return NextResponse.json({ client_secret: session.client_secret, expires_at: session.expires_at });
  } catch (e: any) {
    return NextResponse.json({ error: e?.message || "session error" }, { status: 500 });
  }
}

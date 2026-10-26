/** Validate a Responses web_search result before displaying sourced claims. */
export type SearchResult = { answer: string; sources: string[] };

type ObjectValue = Record<string, unknown>;

function asObject(value: unknown): ObjectValue | null {
  return value !== null && typeof value === "object" && !Array.isArray(value)
    ? value as ObjectValue : null;
}

function validSourceUrl(value: unknown): value is string {
  if (typeof value !== "string" || /\s/.test(value)) return false;
  try {
    const parsed = new URL(value);
    return (parsed.protocol === "https:" || parsed.protocol === "http:") && Boolean(parsed.hostname);
  } catch {
    return false;
  }
}

export function validateWebSearchResponse(response: unknown): SearchResult {
  const result = asObject(response);
  const items = result?.output;
  if (result?.status !== "completed" || !Array.isArray(items)) {
    throw new Error("Web search response did not complete.");
  }
  const calls = items.filter((item: unknown) => asObject(item)?.type === "web_search_call");
  if (!calls.length || calls.some((item: unknown) => asObject(item)?.status !== "completed")) {
    throw new Error("Web search tool call did not complete.");
  }
  const answer = result.output_text;
  if (typeof answer !== "string" || !answer.trim()) {
    throw new Error("Web search returned an empty answer.");
  }

  const sources = new Set<string>();
  for (const item of items) {
    const message = asObject(item);
    if (message?.type !== "message" || !Array.isArray(message.content)) continue;
    for (const part of message.content) {
      const text = asObject(part);
      if (text?.type !== "output_text" || !Array.isArray(text.annotations)) continue;
      for (const annotation of text.annotations) {
        const citation = asObject(annotation);
        if (citation?.type === "url_citation" && validSourceUrl(citation.url)) {
          sources.add(citation.url);
        }
      }
    }
  }
  if (!sources.size) {
    throw new Error("Web search answer has no valid source citations.");
  }
  return { answer, sources: [...sources] };
}

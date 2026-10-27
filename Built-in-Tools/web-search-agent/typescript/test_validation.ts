import assert from "node:assert/strict";
import test from "node:test";
import { validateWebSearchResponse } from "./validation.ts";

function fixture(overrides: Record<string, unknown> = {}) {
  return {
    status: "completed",
    output_text: "Sourced answer.",
    output: [
      { type: "web_search_call", status: "completed", action: { type: "search" } },
      { type: "message", content: [
        { type: "output_text", annotations: [
          { type: "url_citation", url: "https://example.org/article" },
          { type: "url_citation", url: "https://example.org/article" },
        ] },
      ] },
    ],
    ...overrides,
  };
}

test("accepts completed, cited search and deduplicates sources", () => {
  assert.deepEqual(validateWebSearchResponse(fixture()), {
    answer: "Sourced answer.", sources: ["https://example.org/article"],
  });
});

test("rejects completed web tool calls without an actual search action", () => {
  const message = fixture().output[1];
  for (const action of ["open_page", "find_in_page", undefined]) {
    const output = [{ type: "web_search_call", status: "completed", action: action && { type: action } }, message];
    assert.throws(() => validateWebSearchResponse(fixture({ output })), /no search action/);
  }
});

test("rejects incomplete response and failed or missing search calls", () => {
  assert.throws(() => validateWebSearchResponse(fixture({ status: "incomplete" })), /did not complete/);
  assert.throws(() => validateWebSearchResponse(fixture({ output: [
    { type: "web_search_call", status: "failed" },
  ] })), /tool call did not complete/);
  assert.throws(() => validateWebSearchResponse(fixture({ output: [
    { type: "message", content: [] },
  ] })), /tool call did not complete/);
});

test("rejects missing, malformed or non-web citations", () => {
  for (const url of ["javascript:alert(1)", "https://", "https://bad domain.test"]) {
    const output = [
      { type: "web_search_call", status: "completed" },
      { type: "message", content: [{ type: "output_text", annotations: [
        { type: "url_citation", url },
      ] }] },
    ];
    assert.throws(() => validateWebSearchResponse(fixture({ output })), /no valid source citations/);
  }
});

test("rejects empty answer even when search succeeded", () => {
  assert.throws(() => validateWebSearchResponse(fixture({ output_text: "  " })), /empty answer/);
});

# Quickstart: OpenAI Agent Builder

**Goal:** Create and publish a simple workflow in Agent Builder, then connect it to ChatKit.

## Steps
1. **Create a workflow**
   - Open Agent Builder and create a new workflow from a starter template.
   - Add system instructions and a short example.
2. **Add tools**
   - Enable **Web Search** for up-to-date answers.
   - (Optional) Connect **File Search** to an OpenAI Vector Store with your docs.
3. **Guardrails (optional)**
   - Add simple input/output checks if your surface is public.
4. **Publish**
   - Publish the workflow and copy its **Workflow ID** (e.g., `wf_...`).
5. **Embed with ChatKit**
   - Use the `chatkit-ui-template` to pass `WORKFLOW_ID` and render the widget.

## Tips
- Keep instructions short and test with realistic prompts.
- Use hosted tools for speed before integrating custom APIs.
- When the workflow stabilizes, embed via ChatKit in your app.

## References
- AgentKit / Agent Builder overview and built-in tools/web search.
- ChatKit overview and authentication.

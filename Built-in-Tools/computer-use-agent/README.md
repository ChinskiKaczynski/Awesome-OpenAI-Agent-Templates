# Computer Use Agent (incomplete scaffold)

> **Not a working computer-use agent.** The included Python and TypeScript scripts send a single Responses API request, but do not launch a browser/desktop, execute returned actions, capture screenshots, or continue the tool loop. They cannot complete the advertised tasks. Do not treat their output as verified task success or use them in production.

## Current API

These examples still use the older `computer_use_preview` tool with `gpt-4o-mini`. They have **not** been migrated or integration-tested against the current computer-use API. The current OpenAI guide uses the `computer` tool with a supported model and requires an environment driver that executes actions and returns screenshots.

For a working integration, follow the [official Computer Use guide](https://developers.openai.com/api/docs/guides/tools-computer-use), including the action/screenshot loop, or start from its linked sample app. Do not run these scripts expecting them to automate a browser; their API calls may incur charges.

## What is missing

1. A sandboxed, persistent browser or desktop driver.
2. Execution of each returned `computer_call` action in order.
3. A `computer_call_output` screenshot returned with the matching `call_id`, followed by additional Responses turns until completion.
4. Step limits, user confirmation for consequential actions, and verification of the final UI state.

## Safety

- Run computer actions only in an isolated environment with restricted access.
- Never expose sensitive credentials or permit unapproved purchases, submissions, or destructive changes.
- Treat page content as untrusted; verify actual UI state before reporting success.

**Status:** Historical illustrative scaffold only. No successful end-to-end smoke test is claimed.

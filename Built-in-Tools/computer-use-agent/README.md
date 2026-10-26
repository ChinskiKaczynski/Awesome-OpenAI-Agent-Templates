# Computer Use Agent — restricted Python browser demo

**Python:** A bounded Playwright example based on the [current OpenAI computer-tool guide](https://developers.openai.com/api/docs/guides/tools-computer-use). It uses a fictional parcel-pickup page, blocks page network access and permits *only screenshots and left-clicks on one specific disclosure control*. It verifies actual DOM state before reporting success. The \`--live\` mode uses the SDK's \`AsyncComputerToolset\` to execute computer actions and return screenshots across Responses turns, with \`max_steps=6\` and \`store=False\`.

**TypeScript:** \`typescript/main.ts\` remains a **legacy, non-working scaffold** using \`computer_use_preview\` and has not been migrated. Do not execute it expecting browser automation.

## 1. Install Python dependencies

From \`Built-in-Tools/computer-use-agent/python/\`:

\`\`\`bash
python -m venv .venv
# Activate .venv according to your OS, then:
python -m pip install -r requirements.txt
python -m playwright install chromium
\`\`\`

Playwright requires its Chromium runtime (and on some Linux machines, system libraries). On Windows, \`py -3\` is an alternative to \`python\`.

## 2. Free, offline browser smoke test (default)

\`\`\`bash
python main.py
python -m unittest -v test_computer.py
\`\`\`

These run a **real local Chromium browser**, capture a screenshot, click the permitted element and confirm it opened. They **never instantiate an OpenAI API client**, do not require a key or network access, and cannot validate model-driven behavior. The page has no external content or credentials. For a system-installed Chromium, you may set \`PLAYWRIGHT_CHROMIUM_EXECUTABLE\` to its full path instead of downloading Playwright's copy.

## 3. Optional live model integration (billable; requires separate approval)

**Do not use this in automated CI.** Ensure your API project has access to a [computer-capable model](https://developers.openai.com/api/docs/guides/tools-computer-use), check pricing and set \`OPENAI_API_KEY\` in your local environment. Then explicitly run:

\`\`\`bash
python main.py --live
\`\`\`

\`--live\` is **not** the default. The model in the example is \`gpt-6.1-sol\`, matching the current official guide; availability depends on project access and may change. There are at most six tool turns, but usage can still incur charges. A real API integration test has **not** been performed.

## Boundaries and caveats

- **Not a general web scraper or production browser agent.** There is no arbitrary navigation, login, form submission or external network request. Only a local fixture page is used.
- Browser context is ephemeral. Page requests are blocked, and local credentials are never provided. This is application-level isolation; **use a secure container or separate OS sandbox for untrusted execution**, as browser sandboxing depends on platform configuration.
- Only screenshots and a narrowly restricted left click are allowed; \`click()\` independently checks the target again. All other actions are rejected.
- The SDK's computer toolset handles the action/screenshot/response loop in live mode. A test with the real OpenAI service and model has **not** been run.
- For more complex interactions, add explicit per-action approval, URL policies and a controlled environment before enabling any real-world navigation or side effects.

"""Bounded Computer Use demo on an isolated, network-blocked Playwright page.

By default runs a free local browser smoke test. --live explicitly opts in to
billable Responses calls, and is restricted to screenshots and one safe click.
"""
import argparse
import asyncio
import base64
import os
from types import SimpleNamespace

from playwright.async_api import async_playwright

PAGE_HTML = """<!doctype html><html lang="en"><meta charset="utf-8">
<title>Fictional parcel pickup</title><main>
<h1>Fictional parcel pickup</h1><p>Order #1042 is ready.</p>
<details><summary>Show pickup details</summary>
<p>Locker 18. Pickup code: 6249.</p></details></main></html>"""
PROMPT = (
    "Use the computer tool to take a screenshot, then open 'Show pickup details' "
    "and report the locker and pickup code. Only take screenshots or left-click "
    "the 'Show pickup details' control. Never navigate or submit information."
)


class PickupDriver:
    """Only permits screenshots and revalidated clicks on the local summary."""

    def __init__(self, page):
        self.page = page

    async def screenshot(self):
        image = await self.page.screenshot(type="png")
        return {
            "type": "computer_screenshot",
            "image_url": "data:image/png;base64," + base64.b64encode(image).decode("ascii"),
        }

    async def allowed(self, action):
        if action.type == "screenshot":
            return True
        if (action.type != "click" or action.button != "left"
                or getattr(action, "keys", None)):
            return False
        box = await self.page.locator("summary").bounding_box()
        return bool(
            box and box["x"] <= action.x < box["x"] + box["width"]
            and box["y"] <= action.y < box["y"] + box["height"]
        )

    async def click(self, action):
        # Recheck immediately before execution, not only at approval time.
        if not await self.allowed(action):
            raise RuntimeError("Click is outside the permitted local control")
        await self.page.mouse.click(action.x, action.y)

    async def refuse(self, action):
        raise RuntimeError(f"Action not allowed in this demo: {action.type}")

    double_click = drag = keypress = move = scroll = type = wait = refuse


async def verify_details(page):
    if await page.locator("details").get_attribute("open") is None:
        raise RuntimeError("The pickup details were not opened")
    return await page.locator("details p").inner_text()


async def run_demo(live=False):
    if live and not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY before explicitly using --live")

    async with async_playwright() as playwright:
        kwargs = {"headless": True, "env": {}}
        executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
        if executable:
            kwargs["executable_path"] = executable
        browser = await playwright.chromium.launch(**kwargs)
        try:
            page = await browser.new_page(viewport={"width": 1024, "height": 768})
            # All attempted page/subresource requests are blocked.
            await page.route("**/*", lambda route: route.abort())
            await page.set_content(PAGE_HTML)
            driver = PickupDriver(page)
            if live:
                from openai import AsyncComputerToolset, AsyncOpenAI

                async with AsyncOpenAI(timeout=30.0, max_retries=0) as client:
                    tools = AsyncComputerToolset(driver)
                    try:
                        response = await tools.run(
                            client,
                            {"model": "gpt-6.1-sol", "store": False, "input": PROMPT},
                            before_action=driver.allowed,
                            max_steps=6,
                        )
                    finally:
                        tools.close()
                    result = await verify_details(page)
                    print("Verified local browser state:", result)
                    print("Model response:", response.output_text)
                    return result
            else:
                # The same real browser driver, with no SDK client or API request.
                image = await driver.screenshot()
                if not image["image_url"].startswith("data:image/png;base64,"):
                    raise RuntimeError("Screenshot was not captured")
                box = await page.locator("summary").bounding_box()
                if not box:
                    raise RuntimeError("Missing test control")
                click = SimpleNamespace(
                    type="click", button="left", keys=[],
                    x=box["x"] + box["width"] / 2,
                    y=box["y"] + box["height"] / 2,
                )
                await driver.click(click)
                result = await verify_details(page)
                print("Offline browser smoke PASS:", result)
                return result
        finally:
            await browser.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live", action="store_true",
        help="Explicitly opt in to billable OpenAI API calls (never used by default)",
    )
    args = parser.parse_args()
    asyncio.run(run_demo(live=args.live))


if __name__ == "__main__":
    main()

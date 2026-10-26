"""Local browser/driver regression tests. No OpenAI account or network required."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

from playwright.async_api import async_playwright

spec = importlib.util.spec_from_file_location("safe_computer_demo", Path(__file__).with_name("main.py"))
demo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(demo)


class BrowserDriverTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            **demo.browser_launch_options(False)
        )
        self.page = await self.browser.new_page(viewport={"width": 1024, "height": 768})
        await self.page.route("**/*", lambda route: route.abort())
        await self.page.set_content(demo.PAGE_HTML)
        self.driver = demo.PickupDriver(self.page)

    async def asyncTearDown(self):
        await self.browser.close()
        await self.playwright.stop()

    async def test_screenshot_is_real_png(self):
        import base64
        shot = await self.driver.screenshot()
        self.assertEqual(shot["type"], "computer_screenshot")
        self.assertTrue(base64.b64decode(shot["image_url"].split(",", 1)[1]).startswith(b"\x89PNG\r\n\x1a\n"))

    async def test_safe_click_opens_real_local_page(self):
        box = await self.page.locator("summary").bounding_box()
        click = SimpleNamespace(type="click", button="left", keys=[], x=box["x"] + 3, y=box["y"] + 3)
        self.assertTrue(await self.driver.allowed(click))
        await self.driver.click(click)
        self.assertEqual(await demo.verify_details(self.page), "Locker 18. Pickup code: 6249.")

    async def test_unsafe_actions_are_rejected(self):
        for action in [
            SimpleNamespace(type="type", text="steal"),
            SimpleNamespace(type="click", button="right", keys=[], x=5, y=5),
            SimpleNamespace(type="click", button="left", keys=[], x=900, y=700),
            SimpleNamespace(type="click", button="left", keys=["CTRL"], x=10, y=10),
        ]:
            self.assertFalse(await self.driver.allowed(action))
        with self.assertRaisesRegex(RuntimeError, "not allowed"):
            await self.driver.type(SimpleNamespace(type="type", text="private"))
        with self.assertRaisesRegex(RuntimeError, "outside the permitted"):
            await self.driver.click(SimpleNamespace(type="click", button="left", keys=[], x=900, y=700))

    async def test_live_actions_require_chromium_sandbox(self):
        # Offline fixtures can run on CI hosts without unprivileged user namespaces.
        self.assertFalse(demo.browser_launch_options(False)["chromium_sandbox"])
        self.assertTrue(demo.browser_launch_options(True)["chromium_sandbox"])
        self.assertEqual(demo.browser_launch_options(True)["env"], {})

    async def test_unopened_state_is_not_reported_as_success(self):
        with self.assertRaisesRegex(RuntimeError, "not opened"):
            await demo.verify_details(self.page)


if __name__ == "__main__":
    unittest.main()

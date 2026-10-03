import unittest

from app.config import settings


class SettingsTests(unittest.TestCase):
    def test_env_values_are_loaded(self):
        self.assertIsInstance(settings.GEMINI_API_KEY, str)
        self.assertTrue(settings.GEMINI_API_KEY)
        self.assertIsInstance(settings.MODEL_NAME, str)
        self.assertTrue(settings.MODEL_NAME)
        self.assertNotIn("gemini-2.5-flash", settings.MODEL_NAME)
        self.assertTrue(settings.MODEL_NAME.startswith("gemini-"))

    def test_example_env_is_used_as_fallback(self):
        data = settings.load_environment(settings.BASE_DIR / ".env.example")
        self.assertIsInstance(data["GEMINI_API_KEY"], str)
        self.assertTrue(data["GEMINI_API_KEY"])
        self.assertIsInstance(data["MODEL_NAME"], str)
        self.assertTrue(data["MODEL_NAME"].startswith("gemini-"))


if __name__ == "__main__":
    unittest.main()

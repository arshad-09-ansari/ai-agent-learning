
import unittest

from app.day24.dispatcher import dispatch


class DispatcherTests(unittest.TestCase):

    def test_multiply(self):
        result = dispatch(
            "multiply",
            {"a": 10, "b": 5},
        )

        self.assertTrue(result["ok"])
        self.assertEqual(result["result"], 50)

    def test_missing_argument(self):
        result = dispatch(
            "multiply",
            {"a": 10},
        )

        self.assertFalse(result["ok"])
        self.assertIn("Missing arguments", result["error"])

    def test_wrong_type(self):
        result = dispatch(
            "multiply",
            {"a": 10, "b": "five"},
        )

        self.assertFalse(result["ok"])

    def test_unknown_tool(self):
        result = dispatch(
            "delete_database",
            {},
        )

        self.assertFalse(result["ok"])
        self.assertIn("not allowed", result["error"])

    def test_extra_argument(self):
        result = dispatch(
            "add",
            {"a": 2, "b": 3, "admin": True},
        )

        self.assertFalse(result["ok"])
        self.assertIn("Unexpected arguments", result["error"])
def test_subtract(self):
    result = dispatch(
        "subtract",
        {"a": 20, "b": 8},
    )

    self.assertTrue(result["ok"])
    self.assertEqual(result["result"], 12)

def test_nan_rejected(self):
    result = dispatch(
        "multiply",
        {"a": float("nan"), "b": 5},
    )
    self.assertFalse(result["ok"])
    self.assertIn("finite", result["error"])


def test_infinity_rejected(self):
    result = dispatch(
        "multiply",
        {"a": float("inf"), "b": 5},
    )
    self.assertFalse(result["ok"])
    self.assertIn("finite", result["error"])


def test_boolean_rejected(self):
    result = dispatch(
        "multiply",
        {"a": True, "b": 5},
    )
    self.assertFalse(result["ok"])
if __name__ == "__main__":
    unittest.main()

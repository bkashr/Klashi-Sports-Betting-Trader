import unittest
from pathlib import Path


class RepositoryLayoutTests(unittest.TestCase):
    def test_soccer_poisson_test_in_expected_path(self) -> None:
        expected = Path(__file__).resolve().parent / "test_soccer_poisson.py"
        self.assertTrue(expected.exists(), f"Missing expected test file: {expected}")


if __name__ == "__main__":
    unittest.main()

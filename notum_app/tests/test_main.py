import unittest
from notum_app.src.main import main

class TestMain(unittest.TestCase):
    def test_main_runs_without_error(self):
        """
        Tests that the main function runs without raising an exception.
        """
        try:
            main()
            # If main() completes without an exception, the test passes.
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"main() raised an exception unexpectedly: {e}")

if __name__ == '__main__':
    unittest.main()

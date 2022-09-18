import unittest
from main import evaluate_row


class TestEvaluateROW(unittest.TestCase):
    def test_heterogram(self):
        actual = evaluate_row("spits", "since", 1, unittest=True)
        expected = (["Green", "Gray", "Yellow", "Gray", "Gray"], True)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()

import unittest
from main import evaluate_row


class TestEvaluateRow(unittest.TestCase):
    def test_heterogram(self):
        actual = evaluate_row("spits", "since", 1, unittest=True)
        expected = (["Green", "Gray", "Yellow", "Gray", "Gray"])
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()

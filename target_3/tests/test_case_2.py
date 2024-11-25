import unittest
import json
from config_parser import ConfigParser

class TestCalculation(unittest.TestCase):
    def test_calculation_parsing_with_error(self):
        test_input = """
        (define MAX_SIZE 10);
        (define OFFSET 5);
        @(OFFSET 3 - abs)
        """

        expected_data = [
            {"define": {"name": "MAX_SIZE", "value": "10"}},
            {"define": {"name": "OFFSET", "value": "5"}},
        ]

        expected_errors = [
            "ERROR:config_parser:Ошибка вычисления: 5 3 - abs (Неизвестный токен: -)"
        ]


if __name__ == "__main__":
    unittest.main()


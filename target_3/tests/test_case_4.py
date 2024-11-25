import unittest
from config_parser import ConfigParser
import os
import json

class TestMixedStructures(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_mixed.txt"
        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write("""
/# Многострочные структуры #/
(define MAX_SIZE 10);
(define OFFSET 5);
(define NEGATIVE_NUM -10);

@(MAX_SIZE OFFSET +)

({
1, 2, 3, 4
})

({
MAX_SIZE, OFFSET, 100, NEGATIVE_NUM
})
            """)

    def tearDown(self):
        os.remove(self.test_file)

    def test_mixed_parsing(self):
        parser = ConfigParser(self.test_file)
        parser.parse()
        expected_data = [
            {"define": {"name": "MAX_SIZE", "value": "10"}},
            {"define": {"name": "OFFSET", "value": "5"}},
            {"define": {"name": "NEGATIVE_NUM", "value": "-10"}},
            {"calculate": {"expression": "10 5 +", "result": 15}},
            {"array": ["1", "2", "3", "4"]},
            {"array": [10, 5, "100", -10]}
        ]
        self.assertEqual(json.loads(parser.get_json()), expected_data)

if __name__ == "__main__":
    unittest.main()


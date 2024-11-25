import unittest
from config_parser import ConfigParser
import os
import json

class TestDefine(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_define.txt"
        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write("""
/# Определяем константы #/
(define MAX_SIZE 10);
(define OFFSET 5);
(define NEGATIVE_NUM -10);
            """)

    def tearDown(self):
        os.remove(self.test_file)

    def test_define_parsing(self):
        parser = ConfigParser(self.test_file)
        parser.parse()
        expected_data = [
            {"define": {"name": "MAX_SIZE", "value": "10"}},
            {"define": {"name": "OFFSET", "value": "5"}},
            {"define": {"name": "NEGATIVE_NUM", "value": "-10"}}
        ]
        self.assertEqual(json.loads(parser.get_json()), expected_data)

if __name__ == "__main__":
    unittest.main()


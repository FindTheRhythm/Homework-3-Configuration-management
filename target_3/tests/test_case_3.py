import unittest
from config_parser import ConfigParser
import os
import json

class TestArray(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_array.txt"
        with open(self.test_file, "w", encoding="utf-8") as file:
            file.write("""
/# Определяем массивы #/
({
1, 2, 3, 4
})
({
MAX_SIZE, OFFSET, 100, NEGATIVE_NUM
})
            """)

    def tearDown(self):
        os.remove(self.test_file)

    def test_array_parsing(self):
        parser = ConfigParser(self.test_file)
        parser.constants = {"MAX_SIZE": 10, "OFFSET": 5, "NEGATIVE_NUM": -10}
        parser.parse()
        expected_data = [
            {"array": ["1", "2", "3", "4"]},
            {"array": [10, 5, "100", -10]}
        ]
        self.assertEqual(json.loads(parser.get_json()), expected_data)

if __name__ == "__main__":
    unittest.main()


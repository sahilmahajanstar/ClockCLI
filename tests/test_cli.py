import unittest
import argparse
from unittest.mock import patch
from cli import parse_args

class TestCLI(unittest.TestCase):
    @patch('argparse._sys.argv', ['cli.py', 'add', '--title', 'Test', '--type', 'datetime', '--time', '2026-09-23T10:00:00'])
    def test_add_datetime_command(self):
        args = parse_args()
        self.assertEqual(args.command, 'add')
        self.assertEqual(args.title, 'Test')
        self.assertEqual(args.type, 'datetime')
        self.assertEqual(args.time, '2026-09-23T10:00:00')

    @patch('argparse._sys.argv', ['cli.py', 'list'])
    def test_list_command(self):
        args = parse_args()
        self.assertEqual(args.command, 'list')

if __name__ == '__main__':
    unittest.main()

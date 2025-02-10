import os
import unittest
from unittest.mock import patch
import io
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import creatingTgtgCommands

class TestCreatingCommands(unittest.TestCase):
    
    def firstFourLines(self, lines):
        self.assertTrue(lines[0].startswith("access_token:"))
        self.assertTrue(lines[1].startswith("refresh_token:"))
        self.assertTrue(lines[2].startswith("cookie:"))
        self.assertEqual(lines[3], "type:connection\n")
    
    def tearDown(self):
        if os.path.exists("commands.txt"):
            os.remove("commands.txt")
    
    @patch('builtins.input', side_effect=["skip"])
    def test_simpleTest(self, mock_input):
        creatingTgtgCommands.creatingCommands()  # Function call
        with open("commands.txt", "r") as commands:
            lines = commands.readlines()
            self.firstFourLines(lines)
        
    @patch('builtins.input', side_effect=["skip", "11", "y", "4"])
    def test_randomNotification(self, mock_input):
        creatingTgtgCommands.creatingCommands(notification=True)
        
        with open("commands.txt", "r") as commands:
            lines = commands.readlines()
            self.firstFourLines(lines)
            self.assertTrue(lines[4].startswith("item_id:"))
            self.assertEqual(lines[5], "duration:4\n")
            self.assertEqual(lines[6], "type:notify\n")
    
    @patch('builtins.input', side_effect=["skip", "11", "x", "q"])
    def test_quitNotification(self, mock_input):
        creatingTgtgCommands.creatingCommands(notification=True)
        with open("commands.txt", "r") as commands:
            lines = commands.readlines()
            self.firstFourLines(lines)
            self.assertEqual(len(lines), 4)

    

if __name__ == "__main__":
    unittest.main()

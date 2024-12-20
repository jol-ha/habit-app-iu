import unittest
from unittest.mock import patch
import io
from habit_tracker import habit

class TestHabitFunction(unittest.TestCase):
    
    @patch('builtins.input', side_effect=["tdf", "c"])  # Mock user inputs
    @patch('sys.stdout', new_callable=io.StringIO)     # Capture printed output
    def test_habit_tdf_calculation(self, mock_stdout, mock_input):
        """
        Test the habit function with 'tdf' file option and 'c' (calculation) user choice.
        """
        with patch('habit_tracker.calculations.calculations') as mock_calc:
            habit()  # Call the function
            
            # Check if the correct file was used
            output = mock_stdout.getvalue()
            self.assertIn("Using the file: test_data_file.csv", output)
            self.assertIn("You have chosen to analyze your habits.", output)
            
            # Ensure the calculation function was called with the correct file
            mock_calc.assert_called_once_with("test_data_file.csv")
    
    @patch('builtins.input', side_effect=["", "i"])  # Mock user inputs
    @patch('sys.stdout', new_callable=io.StringIO)  # Capture printed output
    def test_habit_default_file_initiation(self, mock_stdout, mock_input):
        """
        Test the habit function with default file and 'i' (initiation) user choice.
        """
        with patch('habit_tracker.initiation.add_habit') as mock_init:
            habit()  # Call the function
            
            # Check if the default file was used
            output = mock_stdout.getvalue()
            self.assertIn("Using the file: raw_data.csv", output)
            self.assertIn("You have chosen initiation.", output)
            
            # Ensure the initiation function was called with the correct file
            mock_init.assert_called_once_with("raw_data.csv")
    
    @patch('builtins.input', side_effect=["custom_file.csv", "e"])  # Mock user inputs
    @patch('sys.stdout', new_callable=io.StringIO)  # Capture printed output
    def test_habit_custom_file_entry(self, mock_stdout, mock_input):
        """
        Test the habit function with a custom file and 'e' (entry) user choice.
        """
        with patch('habit_tracker.entry.enter') as mock_entry:
            habit()  # Call the function
            
            # Check if the custom file was used
            output = mock_stdout.getvalue()
            self.assertIn("Using the file: custom_file.csv", output)
            self.assertIn("You have chosen to make entries.", output)
            
            # Ensure the entry function was called with the correct file
            mock_entry.assert_called_once_with("custom_file.csv")
    
    @patch('builtins.input', side_effect=["", "x"])  # Mock invalid user input
    @patch('sys.stdout', new_callable=io.StringIO)  # Capture printed output
    def test_habit_invalid_choice(self, mock_stdout, mock_input):
        """
        Test the habit function with an invalid user choice.
        """
        habit()  # Call the function
        
        # Check if the invalid input message was printed
        output = mock_stdout.getvalue()
        self.assertIn("Invalid entry. Please user_choice a valid option.", output)


if __name__ == "__main__":
    unittest.main()

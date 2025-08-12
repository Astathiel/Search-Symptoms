import unittest
import os
import csv
from app import main

class TestSymptomMatcher(unittest.TestCase):

    def setUp(self):
        """Set up a temporary test database file and a mock database."""
        self.test_csv_filename = "test_illness_database.csv"
        # Get the directory of the current test file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_csv_filepath = os.path.join(script_dir, self.test_csv_filename)

        # Create a dummy CSV file for testing load_database
        with open(self.test_csv_filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["illness", "symptoms"])
            writer.writerow(["Flu", "fever;body aches;cough;fatigue"])
            writer.writerow(["Common Cold", "sore throat;runny nose;cough;sneezing"])
            writer.writerow(["Allergies", "sneezing;runny nose;itchy eyes"])

        # Create a mock database for testing match_illnesses
        self.mock_database = {
            "Flu": ["fever", "body aches", "cough", "fatigue"],
            "Common Cold": ["sore throat", "runny nose", "cough", "sneezing"],
            "Allergies": ["sneezing", "runny nose", "itchy eyes"],
        }

    def tearDown(self):
        """Remove the temporary test database file."""
        if os.path.exists(self.test_csv_filepath):
            os.remove(self.test_csv_filepath)

    def test_load_database_success(self):
        """Test that the database is loaded correctly from a CSV file."""
        db = main.load_database(self.test_csv_filename)
        self.assertEqual(db, self.mock_database)

    def test_load_database_file_not_found(self):
        """Test that FileNotFoundError is raised for a non-existent file."""
        with self.assertRaises(FileNotFoundError):
            main.load_database("non_existent_file.csv")

    def test_match_illnesses_success(self):
        """Test finding illnesses with sufficient matching symptoms."""
        # These symptoms should match "Common Cold" with 3 matches.
        symptoms = ["Cough", "RUNNY NOSE", "sore throat"]
        results = main.match_illnesses(symptoms, self.mock_database, min_matches=2)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], ("Common Cold", 3))

    def test_match_illnesses_multiple_matches(self):
        """Test that multiple illnesses can be matched and are sorted correctly."""
        # "sneezing" and "runny nose" are in both "Common Cold" and "Allergies"
        symptoms = ["sneezing", "runny nose"]
        results = main.match_illnesses(symptoms, self.mock_database, min_matches=2)
        
        # We expect two results, both with 2 matches.
        self.assertEqual(len(results), 2)
        # The order isn't guaranteed when counts are equal, so we check the contents.
        expected_results = [("Common Cold", 2), ("Allergies", 2)]
        self.assertCountEqual(results, expected_results)

    def test_match_illnesses_sorting(self):
        """Test that results are sorted by match count in descending order."""
        # This should match Flu (3), Common Cold (1)
        symptoms = ["fever", "body aches", "fatigue", "cough"]
        results = main.match_illnesses(symptoms, self.mock_database, min_matches=1)
        
        self.assertEqual(len(results), 2)
        # Flu should be first because it has more matches (4) than Common Cold (1)
        # The function returns the count of the *intersection*, so Flu is 4, Cold is 1.
        self.assertEqual(results[0][0], "Flu")
        self.assertEqual(results[0][1], 4)
        self.assertEqual(results[1][0], "Common Cold")
        self.assertEqual(results[1][1], 1)

    def test_match_illnesses_below_threshold(self):
        """Test that illnesses with fewer matches than min_matches are excluded."""
        # "cough" is in "Flu" and "Common Cold", but we require 2 matches.
        symptoms = ["cough", "headache"]
        results = main.match_illnesses(symptoms, self.mock_database, min_matches=2)
        self.assertEqual(len(results), 0)

    def test_match_illnesses_no_matches(self):
        """Test the function with symptoms that don't match any illness."""
        symptoms = ["dizziness", "nausea"]
        results = main.match_illnesses(symptoms, self.mock_database, min_matches=1)
        self.assertEqual(len(results), 0)

    def test_match_illnesses_empty_input(self):
        """Test the function with an empty list of symptoms."""
        symptoms = []
        results = main.match_illnesses(symptoms, self.mock_database, min_matches=1)
        self.assertEqual(len(results), 0)


if __name__ == '__main__':
    # We need to adjust the path to import from the parent `app` directory
    import sys
    # Assuming the test is run from the root directory (Search-Symptoms)
    # or that 'app' is in the python path.
    # For robust execution, let's ensure the project root is in the path.
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from app import main
    unittest.main()


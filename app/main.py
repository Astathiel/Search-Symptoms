# Import the csv module to parse comma separated value files
import csv
# Import the os module for file path manipulations
import os

def load_database(filename="illness_database.csv"):  # Load illness data from CSV
    """Load symptom data from a CSV file into a dictionary."""
    # Create an empty dictionary that will map an illness to its symptoms
    database = {}
    # Determine the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build an absolute path to the CSV file containing the data
    filepath = os.path.join(script_dir, filename)
    # Open the CSV file for reading. The newline argument avoids blank lines on Windows
    with open(filepath, newline='') as csvfile:
        # Treat each row in the CSV as a dictionary where the keys are the column names
        reader = csv.DictReader(csvfile)
        # Iterate over every row in the CSV
        for row in reader:
            # Grab the illness name from the "illness" column
            illness = row["illness"]
            # Split the symptom list on semicolons, trim whitespace, and convert to lowercase
            symptoms = [s.strip().lower() for s in row["symptoms"].split(";")]
            # Store the symptoms list in the database under the illness key
            database[illness] = symptoms
    # Return the completed dictionary mapping illnesses to lists of symptoms
    return database

def match_illnesses(input_symptoms, database, min_matches=2):  # Compare symptoms
    """Return illnesses that share at least ``min_matches`` with ``input_symptoms``."""
    # Convert the user supplied symptoms to lowercase and store them in a set for fast lookup
    input_set = set(sym.lower() for sym in input_symptoms)
    # Prepare a list that will hold tuples of (illness, number_of_matches)
    matches = []

    # Loop over each illness and its symptom list from the database
    for illness, symptoms in database.items():
        # Count how many of the user's symptoms are in the illness's symptom list
        match_count = len(input_set.intersection(symptoms))
        # If the count meets or exceeds ``min_matches``, record this illness as a potential match
        if match_count >= min_matches:
            matches.append((illness, match_count))

    # Sort illnesses by the number of matching symptoms in descending order and return
    return sorted(matches, key=lambda x: -x[1])

if __name__ == "__main__":  # Execute the following when script is run directly
    # When run as a script, first load the symptom database from disk
    db = load_database()
    # Ask the user to enter symptoms separated by commas and split the response
    symptoms = input("Enter at least 3 symptoms (comma-separated): ").split(",")
    # Remove any extra whitespace and filter out empty entries
    symptoms = [s.strip() for s in symptoms if s.strip()]

    if len(symptoms) < 3:
        # Ensure the user provided enough information to make a match
        print("❌ Please enter at least 3 symptoms.")
    else:
        # Search for illnesses that share at least two symptoms with the user's input
        results = match_illnesses(symptoms, db)
        if results:
            # Print each illness along with how many of the symptoms matched
            print("✅ Possible matches:")
            for illness, count in results:
                print(f"- {illness} (matched {count} symptoms)")
        else:
            # Inform the user that no strong matches were found
            print("⚠️ No strong matches found.")

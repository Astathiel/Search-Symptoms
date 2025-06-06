import csv

def load_database(filename="illness_database.csv"):
    database = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            illness = row["illness"]
            symptoms = [s.strip().lower() for s in row["symptoms"].split(";")]
            database[illness] = symptoms
    return database

def match_illnesses(input_symptoms, database, min_matches=2):
    input_set = set(sym.lower() for sym in input_symptoms)
    matches = []

    for illness, symptoms in database.items():
        match_count = len(input_set.intersection(symptoms))
        if match_count >= min_matches:
            matches.append((illness, match_count))

    return sorted(matches, key=lambda x: -x[1])  # Sort by most matches first

if __name__ == "__main__":
    db = load_database()
    symptoms = input("Enter at least 3 symptoms (comma-separated): ").split(",")
    symptoms = [s.strip() for s in symptoms if s.strip()]

    if len(symptoms) < 3:
        print("❌ Please enter at least 3 symptoms.")
    else:
        results = match_illnesses(symptoms, db)
        if results:
            print("✅ Possible matches:")
            for illness, count in results:
                print(f"- {illness} (matched {count} symptoms)")
        else:
            print("⚠️ No strong matches found.")

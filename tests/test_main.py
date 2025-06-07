import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from main import load_database, match_illnesses


def test_load_database():
    db = load_database()
    assert isinstance(db, dict)
    assert "Flu" in db
    assert "fever" in db["Flu"]


def test_match_illnesses_basic():
    db = load_database()
    symptoms = ["fever", "cough", "fatigue"]
    matches = match_illnesses(symptoms, db)
    assert ("Flu", 3) in matches


def test_match_illnesses_no_match():
    db = load_database()
    matches = match_illnesses(["notasymptom", "anotherfake", "random"], db)
    assert matches == []

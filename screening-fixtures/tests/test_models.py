"""Tests for namegen models."""

from datetime import date

from namegen.models import PersonRecord


def test_person_record_creation():
    """Test basic PersonRecord creation."""
    record = PersonRecord(
        full_name="John Doe",
        first_name="John",
        middle_name=None,
        last_name="Doe",
        gender="male",
        date_of_birth=date(1990, 1, 1),
        place_of_birth="New York",
        nationality="United States",
    )

    assert record.full_name == "John Doe"
    assert record.first_name == "John"
    assert record.middle_name is None
    assert record.last_name == "Doe"
    assert record.gender == "male"
    assert record.date_of_birth == date(1990, 1, 1)
    assert record.place_of_birth == "New York"
    assert record.nationality == "United States"


def test_person_record_with_middle_name():
    """Test PersonRecord with middle name."""
    record = PersonRecord(
        full_name="Jane Mary Smith",
        first_name="Jane",
        middle_name="Mary",
        last_name="Smith",
        gender="female",
        date_of_birth=date(1985, 6, 15),
        place_of_birth="London",
        nationality="United Kingdom",
    )

    assert record.middle_name == "Mary"


def test_person_record_to_dict():
    """Test conversion to dictionary."""
    record = PersonRecord(
        full_name="Alice Johnson",
        first_name="Alice",
        middle_name="Marie",
        last_name="Johnson",
        gender="female",
        date_of_birth=date(1992, 3, 10),
        place_of_birth="Paris",
        nationality="France",
    )

    result = record.to_dict()

    expected = {
        "full_name": "Alice Johnson",
        "first_name": "Alice",
        "middle_name": "Marie",
        "last_name": "Johnson",
        "gender": "female",
        "date_of_birth": "1992-03-10",
        "place_of_birth": "Paris",
        "nationality": "France",
    }

    assert result == expected


def test_person_record_to_dict_no_middle_name():
    """Test conversion to dictionary without middle name."""
    record = PersonRecord(
        full_name="Bob Wilson",
        first_name="Bob",
        middle_name=None,
        last_name="Wilson",
        gender="male",
        date_of_birth=date(1980, 12, 25),
        place_of_birth="Toronto",
        nationality="Canada",
    )

    result = record.to_dict()

    assert result["middle_name"] == ""
    assert result["first_name"] == "Bob"

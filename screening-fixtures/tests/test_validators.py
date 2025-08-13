"""Tests for namegen validators."""

import csv
from datetime import date
from pathlib import Path

import pytest

from namegen.models import PersonRecord
from namegen.validators import RecordValidator


@pytest.fixture
def validator():
    """Create a RecordValidator instance."""
    return RecordValidator()


@pytest.fixture
def valid_record():
    """Create a valid PersonRecord for testing."""
    return PersonRecord(
        full_name="Jane Mary Smith",
        first_name="Jane",
        middle_name="Mary",
        last_name="Smith",
        gender="female",
        date_of_birth=date(1990, 5, 15),
        place_of_birth="London",
        nationality="United Kingdom",
    )


def test_validate_valid_record(validator, valid_record):
    """Test validation of a good record."""
    score = validator.validate_record(valid_record)
    assert score == 1.0


def test_validate_empty_full_name(validator, valid_record):
    """Test validation with empty full name."""
    valid_record.full_name = ""
    score = validator.validate_record(valid_record)
    assert score == 0.0  # Score can't go below 0


def test_validate_empty_first_name(validator, valid_record):
    """Test validation with empty first name."""
    valid_record.first_name = ""
    score = validator.validate_record(valid_record)
    assert score == 0.7


def test_validate_empty_last_name(validator, valid_record):
    """Test validation with empty last name."""
    valid_record.last_name = ""
    score = validator.validate_record(valid_record)
    assert score == 0.7


def test_validate_invalid_gender(validator, valid_record):
    """Test validation with invalid gender."""
    valid_record.gender = "invalid"
    score = validator.validate_record(valid_record)
    assert score == 0.8


def test_validate_name_inconsistency(validator, valid_record):
    """Test validation with name inconsistencies."""
    valid_record.first_name = "NotInFullName"
    valid_record.last_name = "AlsoNotThere"
    score = validator.validate_record(valid_record)
    assert abs(score - 0.4) < 0.01  # Allow for floating point precision


def test_validate_age_too_young(validator, valid_record):
    """Test validation with person too young."""
    valid_record.date_of_birth = date.today()  # 0 years old
    score = validator.validate_record(valid_record)
    assert score == 0.6  # -0.4 for age issue


def test_validate_age_too_old(validator, valid_record):
    """Test validation with person too old."""
    from datetime import timedelta
    valid_record.date_of_birth = date.today() - timedelta(days=90*365)  # 90 years old
    score = validator.validate_record(valid_record)
    assert score == 0.6  # -0.4 for age issue


def test_validate_csv_file_basic(validator, tmp_path):
    """Test basic CSV validation functionality."""
    # Create test CSV file
    csv_file = tmp_path / "test.csv"

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'full_name', 'first_name', 'middle_name', 'last_name',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality'
        ])
        writer.writerow([
            'John Doe', 'John', '', 'Doe',
            'male', '1990-01-01', 'New York', 'United States'
        ])
        writer.writerow([
            'Invalid Record', 'Wrong', '', 'Names',
            'invalid_gender', '2030-01-01', 'Future City', 'Future Land'
        ])

    # Validate the file
    validator.validate_csv_file(csv_file, threshold=0.7)

    # Read back and check results
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 2

    # First row should pass validation
    assert 'score' in rows[0]
    assert 'skip' in rows[0]
    assert float(rows[0]['score']) >= 0.7
    assert rows[0]['skip'] == 'false'

    # Second row should fail validation
    assert float(rows[1]['score']) < 0.7
    assert rows[1]['skip'] == 'true'


def test_validate_csv_file_missing_file(validator):
    """Test validation with non-existent file."""
    fake_path = Path("/nonexistent/file.csv")

    with pytest.raises(FileNotFoundError):
        validator.validate_csv_file(fake_path)


def test_validate_csv_file_malformed_date(validator, tmp_path):
    """Test validation with malformed date."""
    csv_file = tmp_path / "malformed.csv"

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'full_name', 'first_name', 'middle_name', 'last_name',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality'
        ])
        writer.writerow([
            'Bad Date', 'Bad', '', 'Date',
            'male', 'not-a-date', 'City', 'Country'
        ])

    # Should handle malformed data gracefully
    validator.validate_csv_file(csv_file)

    # Check that it was marked as invalid
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert rows[0]['score'] == '0.00'
    assert rows[0]['skip'] == 'true'

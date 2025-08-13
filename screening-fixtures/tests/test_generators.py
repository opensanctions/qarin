"""Tests for namegen generators."""

import random
from datetime import date

from faker import Faker

from namegen.generators import _generate_single_record, generate_records, _generate_cultural_record, _calculate_culture_distribution
from namegen.models import PersonRecord
from namegen.cultures import NameCulture


def test_generate_records_basic():
    """Test basic record generation."""
    records = generate_records(5, seed=42)
    assert len(records) == 5
    assert all(isinstance(r, PersonRecord) for r in records)


def test_generate_records_with_seed():
    """Test generate_records with seed for reproducibility."""
    seed = 42

    # Generate records with same seed
    records1 = generate_records(5, seed=seed)
    records2 = generate_records(5, seed=seed)

    # With same seed, should generate identical records
    for i in range(5):
        assert records1[i].full_name == records2[i].full_name
        assert records1[i].gender == records2[i].gender


def test_generate_single_record():
    """Test generation of a single record."""
    fake = Faker()
    Faker.seed(123)
    random.seed(123)
    record = _generate_single_record(fake, culture=None)

    # Check all fields are populated
    assert record.full_name
    assert record.first_name
    assert record.last_name
    assert record.gender in ["female", "male", "other"]
    assert isinstance(record.date_of_birth, date)
    assert record.place_of_birth
    assert record.nationality

    # Check name consistency
    assert record.first_name in record.full_name
    assert record.last_name in record.full_name


def test_generate_multiple_records():
    """Test generation of multiple records."""
    count = 10
    records = generate_records(count, seed=456)

    assert len(records) == count
    assert all(isinstance(r, PersonRecord) for r in records)

    # Check uniqueness (should be different with different random states)
    full_names = [r.full_name for r in records]
    assert len(set(full_names)) > 1  # At least some should be different


def test_gender_distribution():
    """Test that gender distribution is roughly correct over many samples."""
    records = generate_records(1000, seed=789)

    genders = [r.gender for r in records]
    female_count = genders.count("female")
    male_count = genders.count("male")
    other_count = genders.count("other")

    # Rough distribution check (45/45/10 with some tolerance)
    assert female_count > 300  # Should be around 450
    assert male_count > 300    # Should be around 450
    assert other_count > 50    # Should be around 100


def test_age_range():
    """Test that generated ages are within expected range (18-85)."""
    records = generate_records(100, seed=101112)

    today = date.today()

    for record in records:
        age_days = (today - record.date_of_birth).days
        age_years = age_days / 365.25

        assert 18 <= age_years <= 85, f"Age {age_years} outside expected range"


def test_middle_name_probability():
    """Test that middle names appear with expected frequency."""
    records = generate_records(1000, seed=131415)

    with_middle = sum(1 for r in records if r.middle_name is not None)
    without_middle = sum(1 for r in records if r.middle_name is None)

    # Should be roughly 60% with middle names
    assert with_middle > 400  # Allow some variance
    assert without_middle > 200


def test_generate_cultural_record():
    """Test generation of culture-specific record."""
    record = _generate_cultural_record(NameCulture.EAST_ASIAN)
    
    # Should have all required fields
    assert record.full_name
    assert record.first_name
    assert record.last_name
    assert record.gender in ["female", "male", "other"]
    assert record.place_of_birth
    assert record.nationality
    
    # Name consistency
    assert record.first_name in record.full_name
    assert record.last_name in record.full_name


def test_generate_records_single_culture():
    """Test generating records from single culture."""
    records = generate_records(10, seed=42, culture=NameCulture.SPANISH_PORTUGUESE)
    
    assert len(records) == 10
    assert all(isinstance(r, PersonRecord) for r in records)
    
    # All records should have consistent cultural markers
    # (Note: exact validation would require complex cultural name analysis)
    for record in records:
        assert record.full_name
        assert record.nationality
        assert record.place_of_birth


def test_generate_records_global_distribution():
    """Test generating records with global distribution."""
    records = generate_records(100, seed=123, distribution="global")
    
    assert len(records) == 100
    assert all(isinstance(r, PersonRecord) for r in records)
    
    # Should have diversity in nationalities (not all the same)
    nationalities = [r.nationality for r in records]
    unique_nationalities = set(nationalities)
    assert len(unique_nationalities) > 5  # Should have significant diversity


def test_generate_records_us_distribution():
    """Test generating records with US distribution."""
    records = generate_records(100, seed=456, distribution="us")
    
    assert len(records) == 100
    assert all(isinstance(r, PersonRecord) for r in records)
    
    # Should have diversity but different from global
    nationalities = [r.nationality for r in records]
    unique_nationalities = set(nationalities)
    assert len(unique_nationalities) > 3  # Should have some diversity


def test_calculate_culture_distribution():
    """Test culture distribution calculation."""
    # Test global distribution
    global_dist = _calculate_culture_distribution(100, "global")
    assert sum(global_dist.values()) == 100
    assert len(global_dist) == len(NameCulture)
    
    # East Asian should get largest share in global
    assert global_dist[NameCulture.EAST_ASIAN] > global_dist[NameCulture.HEBREW_JEWISH]
    
    # Test US distribution  
    us_dist = _calculate_culture_distribution(100, "us")
    assert sum(us_dist.values()) == 100
    assert len(us_dist) == len(NameCulture)
    
    # Western European should get largest share in US
    assert us_dist[NameCulture.WESTERN_EUROPEAN] > us_dist[NameCulture.EAST_ASIAN]


def test_calculate_culture_distribution_edge_cases():
    """Test culture distribution with edge cases."""
    # Small count
    small_dist = _calculate_culture_distribution(1, "global")
    assert sum(small_dist.values()) == 1
    
    # Large count
    large_dist = _calculate_culture_distribution(10000, "us")
    assert sum(large_dist.values()) == 10000
    
    # Invalid distribution
    try:
        _calculate_culture_distribution(100, "invalid")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Unknown distribution" in str(e)


def test_generate_records_parameter_combinations():
    """Test different parameter combinations."""
    # Culture overrides distribution
    records = generate_records(
        10, seed=789, 
        culture=NameCulture.SLAVIC_ORTHODOX, 
        distribution="us"
    )
    assert len(records) == 10
    # Should use culture, not distribution (hard to test directly)
    
    # Default distribution
    records = generate_records(5, seed=101)
    assert len(records) == 5
    
    # Explicit None culture with distribution
    records = generate_records(5, seed=102, culture=None, distribution="global")
    assert len(records) == 5

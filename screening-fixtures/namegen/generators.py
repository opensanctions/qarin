"""Name generation utilities using faker and other sources."""

import random
from datetime import date, timedelta
from typing import List

from faker import Faker

from namegen.models import PersonRecord
from namegen.cultures import NameCulture, CULTURE_PERCENTAGES, US_PERCENTAGES
from namegen.culture_mappings import (
    get_random_locale,
    get_random_nationality, 
    get_random_city,
)


def generate_records(
    count: int, 
    seed: int | None = None,
    culture: NameCulture | None = None,
    distribution: str | None = None,
) -> list[PersonRecord]:
    """Generate a list of synthetic person records.
    
    Args:
        count: Number of records to generate
        seed: Random seed for reproducibility
        culture: Single culture to generate (overrides distribution)
        distribution: 'global', 'us', or None. Ignored if culture is specified.
    
    Returns:
        List of generated PersonRecord objects
    """
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)

    records = []
    
    if culture is not None:
        # Generate all records from single culture
        for _ in range(count):
            record = _generate_cultural_record(culture)
            records.append(record)
    else:
        # Generate records according to distribution
        culture_counts = _calculate_culture_distribution(count, distribution)
        
        for target_culture, target_count in culture_counts.items():
            for _ in range(target_count):
                record = _generate_cultural_record(target_culture)
                records.append(record)
    
    # Shuffle to avoid cultural clustering
    random.shuffle(records)
    return records


def _generate_cultural_record(culture: NameCulture) -> PersonRecord:
    """Generate a single person record for a specific culture."""
    # Get culture-appropriate faker locale
    locale = get_random_locale(culture)
    fake = Faker(locale)
    
    return _generate_single_record(fake, culture)


def _generate_single_record(fake: Faker, culture: NameCulture | None = None) -> PersonRecord:
    """Generate a single person record."""
    # Choose gender first to influence name generation
    gender = random.choices(
        ["female", "male", "other"],
        weights=[45, 45, 10]
    )[0]

    # Generate names based on gender
    if gender == "female":
        first_name = fake.first_name_female()
    elif gender == "male":
        first_name = fake.first_name_male()
    else:
        # For "other", randomly pick from either
        first_name = fake.first_name()

    last_name = fake.last_name()

    # Middle name with 60% probability
    middle_name = fake.first_name() if random.random() < 0.6 else None

    # Build full name
    if middle_name:
        full_name = f"{first_name} {middle_name} {last_name}"
    else:
        full_name = f"{first_name} {last_name}"

    # Generate age between 18 and 85
    age_days = random.randint(18 * 365, 85 * 365)
    date_of_birth = date.today() - timedelta(days=age_days)

    # Generate location data
    if culture is not None:
        place_of_birth = get_random_city(culture)
        nationality = get_random_nationality(culture)
    else:
        place_of_birth = fake.city()
        nationality = fake.country()

    return PersonRecord(
        full_name=full_name,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        gender=gender,
        date_of_birth=date_of_birth,
        place_of_birth=place_of_birth,
        nationality=nationality,
    )


def _calculate_culture_distribution(
    total_count: int, 
    distribution: str | None = None
) -> dict[NameCulture, int]:
    """Calculate how many records to generate for each culture based on distribution."""
    if distribution == "us":
        percentages = US_PERCENTAGES
    elif distribution == "global" or distribution is None:
        percentages = CULTURE_PERCENTAGES  
    else:
        raise ValueError(f"Unknown distribution '{distribution}'. Must be 'global' or 'us'.")
    
    # Calculate target counts for each culture
    culture_counts: dict[NameCulture, int] = {}
    allocated_count = 0
    
    # Sort cultures by percentage (largest first) to handle rounding better
    sorted_cultures = sorted(percentages.keys(), key=lambda c: percentages[c], reverse=True)
    
    for i, culture in enumerate(sorted_cultures):
        if i == len(sorted_cultures) - 1:
            # Last culture gets all remaining records
            culture_counts[culture] = total_count - allocated_count
        else:
            # Calculate proportional count with floor to avoid overshooting
            target_count = int(total_count * percentages[culture] / 100.0)
            culture_counts[culture] = target_count
            allocated_count += target_count
    
    return culture_counts

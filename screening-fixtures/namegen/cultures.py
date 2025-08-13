"""Name culture classifications and demographics."""

from enum import Enum

__all__ = [
    "NameCulture",
    "CULTURE_PERCENTAGES",
    "US_PERCENTAGES",
    "validate_percentages",
    "get_culture_weight",
    "get_all_cultures",
]


class NameCulture(Enum):
    """Enumeration of major sociocultural name families worldwide."""

    EAST_ASIAN = "east_asian"
    ARABIC_ISLAMIC = "arabic_islamic"
    SOUTH_ASIAN = "south_asian"
    WESTERN_EUROPEAN = "western_european"
    SUB_SAHARAN_AFRICAN = "sub_saharan_african"
    SPANISH_PORTUGUESE = "spanish_portuguese"
    SOUTHEAST_ASIAN = "southeast_asian"
    SLAVIC_ORTHODOX = "slavic_orthodox"
    IRANIAN_PERSIAN = "iranian_persian"
    TURKISH_ALTAIC = "turkish_altaic"
    INDIGENOUS_TRADITIONAL = "indigenous_traditional"
    HEBREW_JEWISH = "hebrew_jewish"


# Population percentages based on research from NAME_CULTURES.md
# Raw percentages from research (sum to ~102.3% due to rounding)
_RAW_PERCENTAGES: dict[NameCulture, float] = {
    NameCulture.EAST_ASIAN: 21.0,
    NameCulture.ARABIC_ISLAMIC: 15.0,
    NameCulture.SOUTH_ASIAN: 15.0,
    NameCulture.WESTERN_EUROPEAN: 12.0,
    NameCulture.SUB_SAHARAN_AFRICAN: 12.0,
    NameCulture.SPANISH_PORTUGUESE: 8.0,
    NameCulture.SOUTHEAST_ASIAN: 6.0,
    NameCulture.SLAVIC_ORTHODOX: 6.0,
    NameCulture.IRANIAN_PERSIAN: 3.0,
    NameCulture.TURKISH_ALTAIC: 2.0,
    NameCulture.INDIGENOUS_TRADITIONAL: 2.0,
    NameCulture.HEBREW_JEWISH: 0.3,
}

# Normalize percentages to sum to exactly 100%
_total = sum(_RAW_PERCENTAGES.values())
CULTURE_PERCENTAGES: dict[NameCulture, float] = {
    culture: (percentage / _total) * 100.0
    for culture, percentage in _RAW_PERCENTAGES.items()
}

# US-specific name culture distribution based on Census data and demographic analysis
# Raw percentages from NAME_CULTURES.md US section
_US_RAW_PERCENTAGES: dict[NameCulture, float] = {
    NameCulture.WESTERN_EUROPEAN: 45.0,
    NameCulture.SPANISH_PORTUGUESE: 20.0,
    NameCulture.SUB_SAHARAN_AFRICAN: 14.0,
    NameCulture.EAST_ASIAN: 7.5,
    NameCulture.ARABIC_ISLAMIC: 2.0,
    NameCulture.HEBREW_JEWISH: 1.8,
    NameCulture.INDIGENOUS_TRADITIONAL: 1.5,
    NameCulture.SLAVIC_ORTHODOX: 1.5,
    NameCulture.SOUTH_ASIAN: 1.5,
    NameCulture.IRANIAN_PERSIAN: 0.3,
    # Remaining cultures have minimal presence in US
    NameCulture.SOUTHEAST_ASIAN: 0.5,
    NameCulture.TURKISH_ALTAIC: 0.4,
}

# Normalize US percentages to sum to exactly 100%
_us_total = sum(_US_RAW_PERCENTAGES.values())
US_PERCENTAGES: dict[NameCulture, float] = {
    culture: (percentage / _us_total) * 100.0
    for culture, percentage in _US_RAW_PERCENTAGES.items()
}


def validate_percentages(region: str = "both") -> bool:
    """Validate that culture percentages sum to exactly 100%.

    Args:
        region: 'global', 'us', or 'both' (default) to validate
    """
    if region in ("global", "both"):
        global_total = sum(CULTURE_PERCENTAGES.values())
        global_valid = abs(global_total - 100.0) < 1e-10
        if region == "global":
            return global_valid

    if region in ("us", "both"):
        us_total = sum(US_PERCENTAGES.values())
        us_valid = abs(us_total - 100.0) < 1e-10
        if region == "us":
            return us_valid

    if region == "both":
        return global_valid and us_valid

    raise ValueError(f"Unknown region '{region}'. Must be 'global', 'us', or 'both'.")


def get_culture_weight(culture: NameCulture, region: str = "global") -> float:
    """Get the demographic weight for a given name culture.

    Args:
        culture: The name culture to get weight for
        region: Either 'global' (default) or 'us' for region-specific weights
    """
    if region == "us":
        return US_PERCENTAGES[culture]
    elif region == "global":
        return CULTURE_PERCENTAGES[culture]
    else:
        raise ValueError(f"Unknown region '{region}'. Must be 'global' or 'us'.")


def get_all_cultures(region: str = "global") -> list[NameCulture]:
    """Get list of all name cultures sorted by population percentage (descending).

    Args:
        region: Either 'global' (default) or 'us' for region-specific sorting
    """
    if region == "us":
        percentages = US_PERCENTAGES
    elif region == "global":
        percentages = CULTURE_PERCENTAGES
    else:
        raise ValueError(f"Unknown region '{region}'. Must be 'global' or 'us'.")

    return sorted(
        NameCulture,
        key=lambda c: percentages[c],
        reverse=True
    )

"""Tests for namegen cultures module."""


from namegen.cultures import (
    CULTURE_PERCENTAGES,
    US_PERCENTAGES,
    NameCulture,
    get_all_cultures,
    get_culture_weight,
    validate_percentages,
)


def test_name_culture_enum():
    """Test NameCulture enum has expected values."""
    # Check we have 12 cultures as documented
    assert len(NameCulture) == 12

    # Check some key cultures exist
    assert NameCulture.EAST_ASIAN in NameCulture
    assert NameCulture.ARABIC_ISLAMIC in NameCulture
    assert NameCulture.WESTERN_EUROPEAN in NameCulture
    assert NameCulture.HEBREW_JEWISH in NameCulture


def test_culture_percentages_structure():
    """Test culture percentages dict has correct structure."""
    # Should have entry for each enum value
    assert len(CULTURE_PERCENTAGES) == len(NameCulture)

    # All enum values should be keys
    for culture in NameCulture:
        assert culture in CULTURE_PERCENTAGES

    # All values should be positive floats
    for percentage in CULTURE_PERCENTAGES.values():
        assert isinstance(percentage, int | float)
        assert percentage > 0


def test_culture_percentages_values():
    """Test specific culture percentage values (normalized)."""
    # Check highest populations (approximately, since normalized)
    assert abs(CULTURE_PERCENTAGES[NameCulture.EAST_ASIAN] - 20.53) < 0.1
    assert abs(CULTURE_PERCENTAGES[NameCulture.ARABIC_ISLAMIC] - 14.67) < 0.1
    assert abs(CULTURE_PERCENTAGES[NameCulture.SOUTH_ASIAN] - 14.67) < 0.1

    # Check lowest populations
    assert abs(CULTURE_PERCENTAGES[NameCulture.HEBREW_JEWISH] - 0.29) < 0.1
    assert CULTURE_PERCENTAGES[NameCulture.INDIGENOUS_TRADITIONAL] < 2.0
    assert CULTURE_PERCENTAGES[NameCulture.TURKISH_ALTAIC] < 2.0


def test_validate_percentages():
    """Test that percentages sum to exactly 100%."""
    assert validate_percentages() is True
    assert validate_percentages("global") is True
    assert validate_percentages("us") is True
    assert validate_percentages("both") is True

    # Test the actual sums
    global_total = sum(CULTURE_PERCENTAGES.values())
    us_total = sum(US_PERCENTAGES.values())
    assert abs(global_total - 100.0) < 1e-10
    assert abs(us_total - 100.0) < 1e-10


def test_get_culture_weight():
    """Test get_culture_weight function."""
    # Test global normalized values (approximately)
    assert abs(get_culture_weight(NameCulture.EAST_ASIAN, "global") - 20.53) < 0.1
    assert abs(get_culture_weight(NameCulture.HEBREW_JEWISH, "global") - 0.29) < 0.1

    # Test US values (normalized)
    assert abs(get_culture_weight(NameCulture.WESTERN_EUROPEAN, "us") - 46.88) < 0.1
    assert abs(get_culture_weight(NameCulture.SPANISH_PORTUGUESE, "us") - 20.83) < 0.1

    # Test all cultures have weights for both regions
    for culture in NameCulture:
        global_weight = get_culture_weight(culture, "global")
        us_weight = get_culture_weight(culture, "us")
        assert isinstance(global_weight, int | float)
        assert isinstance(us_weight, int | float)
        assert global_weight > 0
        assert us_weight > 0


def test_get_all_cultures():
    """Test get_all_cultures returns sorted list."""
    # Test global sorting (default)
    global_cultures = get_all_cultures()
    assert len(global_cultures) == len(NameCulture)
    assert set(global_cultures) == set(NameCulture)

    global_percentages = [CULTURE_PERCENTAGES[c] for c in global_cultures]
    assert global_percentages == sorted(global_percentages, reverse=True)
    assert global_cultures[0] == NameCulture.EAST_ASIAN
    assert global_cultures[-1] == NameCulture.HEBREW_JEWISH

    # Test US sorting
    us_cultures = get_all_cultures("us")
    assert len(us_cultures) == len(NameCulture)
    assert set(us_cultures) == set(NameCulture)

    us_percentages = [US_PERCENTAGES[c] for c in us_cultures]
    assert us_percentages == sorted(us_percentages, reverse=True)
    assert us_cultures[0] == NameCulture.WESTERN_EUROPEAN
    assert us_cultures[1] == NameCulture.SPANISH_PORTUGUESE


def test_percentages_sum_to_expected():
    """Test that percentages sum to exactly 100% after normalization."""
    total = sum(CULTURE_PERCENTAGES.values())
    # After normalization, should sum to exactly 100%
    assert abs(total - 100.0) < 1e-10


def test_enum_string_values():
    """Test enum string values are consistent."""
    # Check some key string values
    assert NameCulture.EAST_ASIAN.value == "east_asian"
    assert NameCulture.ARABIC_ISLAMIC.value == "arabic_islamic"
    assert NameCulture.WESTERN_EUROPEAN.value == "western_european"

    # All should be lowercase with underscores
    for culture in NameCulture:
        value = culture.value
        assert value.islower()
        assert " " not in value  # Should use underscores, not spaces


def test_us_percentages_structure():
    """Test US percentages dict has correct structure."""
    # Should have entry for each enum value
    assert len(US_PERCENTAGES) == len(NameCulture)

    # All enum values should be keys
    for culture in NameCulture:
        assert culture in US_PERCENTAGES

    # All values should be positive floats
    for percentage in US_PERCENTAGES.values():
        assert isinstance(percentage, int | float)
        assert percentage > 0


def test_us_percentages_values():
    """Test specific US percentage values (normalized)."""
    # Check highest US populations (normalized from 96% to 100%)
    assert abs(US_PERCENTAGES[NameCulture.WESTERN_EUROPEAN] - 46.88) < 0.1
    assert abs(US_PERCENTAGES[NameCulture.SPANISH_PORTUGUESE] - 20.83) < 0.1
    assert abs(US_PERCENTAGES[NameCulture.SUB_SAHARAN_AFRICAN] - 14.58) < 0.1

    # Check lowest US populations
    assert US_PERCENTAGES[NameCulture.IRANIAN_PERSIAN] < 1.0
    assert US_PERCENTAGES[NameCulture.TURKISH_ALTAIC] < 1.0
    assert US_PERCENTAGES[NameCulture.SOUTHEAST_ASIAN] < 1.0


def test_global_vs_us_differences():
    """Test that global and US distributions are meaningfully different."""
    # East Asian should be much higher globally than in US
    assert CULTURE_PERCENTAGES[NameCulture.EAST_ASIAN] > US_PERCENTAGES[NameCulture.EAST_ASIAN]

    # Western European should be much higher in US than globally
    assert US_PERCENTAGES[NameCulture.WESTERN_EUROPEAN] > CULTURE_PERCENTAGES[NameCulture.WESTERN_EUROPEAN]

    # Spanish-Portuguese should be higher in US than globally
    assert US_PERCENTAGES[NameCulture.SPANISH_PORTUGUESE] > CULTURE_PERCENTAGES[NameCulture.SPANISH_PORTUGUESE]


def test_function_parameter_validation():
    """Test that functions properly validate region parameters."""
    from pytest import raises

    # Test invalid region in get_culture_weight
    with raises(ValueError, match="Unknown region"):
        get_culture_weight(NameCulture.EAST_ASIAN, "invalid")

    # Test invalid region in get_all_cultures
    with raises(ValueError, match="Unknown region"):
        get_all_cultures("invalid")

    # Test invalid region in validate_percentages
    with raises(ValueError, match="Unknown region"):
        validate_percentages("invalid")

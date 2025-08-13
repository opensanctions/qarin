"""Tests for namegen culture mappings."""

from namegen.culture_mappings import (
    CULTURE_LOCALES,
    CULTURE_NATIONALITIES,
    CULTURE_CITIES,
    get_random_locale,
    get_random_nationality,
    get_random_city,
)
from namegen.cultures import NameCulture


def test_culture_locales_completeness():
    """Test that all cultures have locale mappings."""
    assert len(CULTURE_LOCALES) == len(NameCulture)
    
    for culture in NameCulture:
        assert culture in CULTURE_LOCALES
        assert len(CULTURE_LOCALES[culture]) > 0
        assert all(isinstance(locale, str) for locale in CULTURE_LOCALES[culture])


def test_culture_nationalities_completeness():
    """Test that all cultures have nationality mappings."""
    assert len(CULTURE_NATIONALITIES) == len(NameCulture)
    
    for culture in NameCulture:
        assert culture in CULTURE_NATIONALITIES
        assert len(CULTURE_NATIONALITIES[culture]) > 0
        assert all(isinstance(nationality, str) for nationality in CULTURE_NATIONALITIES[culture])


def test_culture_cities_completeness():
    """Test that all cultures have city mappings."""
    assert len(CULTURE_CITIES) == len(NameCulture)
    
    for culture in NameCulture:
        assert culture in CULTURE_CITIES
        assert len(CULTURE_CITIES[culture]) > 0
        assert all(isinstance(city, str) for city in CULTURE_CITIES[culture])


def test_specific_culture_mappings():
    """Test specific culture mappings are reasonable."""
    # East Asian should have Chinese, Japanese, Korean locales
    east_asian_locales = CULTURE_LOCALES[NameCulture.EAST_ASIAN]
    assert "zh_CN" in east_asian_locales
    assert "ja_JP" in east_asian_locales
    assert "ko_KR" in east_asian_locales
    
    # Arabic-Islamic should have Arabic locales
    arabic_locales = CULTURE_LOCALES[NameCulture.ARABIC_ISLAMIC]
    assert any("ar_" in locale for locale in arabic_locales)
    
    # Western European should have major European locales
    western_locales = CULTURE_LOCALES[NameCulture.WESTERN_EUROPEAN]
    assert "en_US" in western_locales
    assert "de_DE" in western_locales
    assert "fr_FR" in western_locales


def test_nationality_cultural_consistency():
    """Test that nationalities match cultural expectations."""
    # East Asian should have Asian countries
    east_asian_nations = CULTURE_NATIONALITIES[NameCulture.EAST_ASIAN]
    assert "China" in east_asian_nations
    assert "Japan" in east_asian_nations
    assert "South Korea" in east_asian_nations
    
    # Spanish-Portuguese should have Latin American and Iberian countries
    hispanic_nations = CULTURE_NATIONALITIES[NameCulture.SPANISH_PORTUGUESE]
    assert "Mexico" in hispanic_nations
    assert "Spain" in hispanic_nations
    assert "Brazil" in hispanic_nations
    
    # Western European should have European and diaspora countries
    western_nations = CULTURE_NATIONALITIES[NameCulture.WESTERN_EUROPEAN]
    assert "United States" in western_nations
    assert "Germany" in western_nations
    assert "France" in western_nations


def test_city_cultural_consistency():
    """Test that cities match cultural expectations."""
    # East Asian should have major Asian cities
    east_asian_cities = CULTURE_CITIES[NameCulture.EAST_ASIAN]
    assert "Beijing" in east_asian_cities
    assert "Tokyo" in east_asian_cities
    assert "Seoul" in east_asian_cities
    
    # Arabic-Islamic should have Middle Eastern/Islamic cities
    arabic_cities = CULTURE_CITIES[NameCulture.ARABIC_ISLAMIC]
    assert "Cairo" in arabic_cities
    assert "Istanbul" in arabic_cities
    assert "Tehran" in arabic_cities


def test_get_random_locale():
    """Test get_random_locale function."""
    # Test valid culture
    locale = get_random_locale(NameCulture.EAST_ASIAN)
    assert locale in CULTURE_LOCALES[NameCulture.EAST_ASIAN]
    
    # Test multiple calls return consistent types
    for _ in range(10):
        locale = get_random_locale(NameCulture.WESTERN_EUROPEAN)
        assert isinstance(locale, str)
        assert locale in CULTURE_LOCALES[NameCulture.WESTERN_EUROPEAN]


def test_get_random_nationality():
    """Test get_random_nationality function."""
    # Test valid culture
    nationality = get_random_nationality(NameCulture.SPANISH_PORTUGUESE)
    assert nationality in CULTURE_NATIONALITIES[NameCulture.SPANISH_PORTUGUESE]
    
    # Test multiple calls return consistent types
    for _ in range(10):
        nationality = get_random_nationality(NameCulture.SOUTH_ASIAN)
        assert isinstance(nationality, str)
        assert nationality in CULTURE_NATIONALITIES[NameCulture.SOUTH_ASIAN]


def test_get_random_city():
    """Test get_random_city function."""
    # Test valid culture
    city = get_random_city(NameCulture.SLAVIC_ORTHODOX)
    assert city in CULTURE_CITIES[NameCulture.SLAVIC_ORTHODOX]
    
    # Test multiple calls return consistent types
    for _ in range(10):
        city = get_random_city(NameCulture.ARABIC_ISLAMIC)
        assert isinstance(city, str)
        assert city in CULTURE_CITIES[NameCulture.ARABIC_ISLAMIC]


def test_locale_format_validity():
    """Test that locale strings follow expected format."""
    for culture, locales in CULTURE_LOCALES.items():
        for locale in locales:
            # Most locales should be in xx_YY format
            if "_" in locale:
                parts = locale.split("_")
                assert len(parts) == 2
                assert len(parts[0]) == 2  # Language code
                assert len(parts[1]) == 2  # Country code
                assert parts[0].islower()
                assert parts[1].isupper()


def test_no_empty_mappings():
    """Test that no culture has empty mappings."""
    for culture in NameCulture:
        assert len(CULTURE_LOCALES[culture]) > 0
        assert len(CULTURE_NATIONALITIES[culture]) > 0
        assert len(CULTURE_CITIES[culture]) > 0


def test_mapping_diversity():
    """Test that cultures have reasonable diversity in mappings."""
    # Most cultures should have multiple options
    cultures_with_single_locale = []
    cultures_with_single_nationality = []
    cultures_with_single_city = []
    
    for culture in NameCulture:
        if len(CULTURE_LOCALES[culture]) == 1:
            cultures_with_single_locale.append(culture)
        if len(CULTURE_NATIONALITIES[culture]) == 1:
            cultures_with_single_nationality.append(culture)
        if len(CULTURE_CITIES[culture]) == 1:
            cultures_with_single_city.append(culture)
    
    # Allow some cultures to have limited options due to faker constraints
    # but most should have multiple choices
    assert len(cultures_with_single_locale) < len(NameCulture) // 2
    assert len(cultures_with_single_nationality) < len(NameCulture) // 3
    assert len(cultures_with_single_city) < len(NameCulture) // 3
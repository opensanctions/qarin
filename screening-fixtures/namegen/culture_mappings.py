"""Mappings from name cultures to locales, nationalities, and cities."""

from namegen.cultures import NameCulture

# Map each culture to appropriate faker locales
# Multiple locales per culture provide variety within cultural boundaries
CULTURE_LOCALES: dict[NameCulture, list[str]] = {
    NameCulture.EAST_ASIAN: [
        "zh_CN",  # Chinese (Simplified)
        "ja_JP",  # Japanese
        "ko_KR",  # Korean
        "zh_TW",  # Chinese (Traditional)
    ],
    NameCulture.ARABIC_ISLAMIC: [
        "ar_SA",  # Arabic (Saudi Arabia)
        "ar_EG",  # Arabic (Egypt)
        "fa_IR",  # Persian (Iran)
        "tr_TR",  # Turkish
    ],
    NameCulture.SOUTH_ASIAN: [
        "hi_IN",  # Hindi (India)
        "ne_NP",  # Nepali (Nepal)
        # Note: faker has limited South Asian locale support
        "en_IN",  # English (India) - fallback for Indian names
    ],
    NameCulture.WESTERN_EUROPEAN: [
        "en_US",  # English (US)
        "en_GB",  # English (UK)
        "de_DE",  # German
        "fr_FR",  # French
        "it_IT",  # Italian
        "nl_NL",  # Dutch
        "sv_SE",  # Swedish
        "no_NO",  # Norwegian
        "da_DK",  # Danish
        "fi_FI",  # Finnish
    ],
    NameCulture.SUB_SAHARAN_AFRICAN: [
        "en_US",  # English - many African countries use English names
        # Note: faker has very limited African locale support
        # Will need custom handling for authentic African names
    ],
    NameCulture.SPANISH_PORTUGUESE: [
        "es_ES",  # Spanish (Spain)
        "es_MX",  # Spanish (Mexico)
        "pt_BR",  # Portuguese (Brazil)
        "pt_PT",  # Portuguese (Portugal)
        "es_AR",  # Spanish (Argentina)
        "es_CO",  # Spanish (Colombia)
    ],
    NameCulture.SOUTHEAST_ASIAN: [
        "th_TH",  # Thai
        "id_ID",  # Indonesian
        # Note: Limited Southeast Asian support in faker
        "en_PH",  # English (Philippines) - fallback
    ],
    NameCulture.SLAVIC_ORTHODOX: [
        "ru_RU",  # Russian
        "pl_PL",  # Polish
        "cs_CZ",  # Czech
        "sk_SK",  # Slovak
        "uk_UA",  # Ukrainian
        "bg_BG",  # Bulgarian
        "hr_HR",  # Croatian
    ],
    NameCulture.IRANIAN_PERSIAN: [
        "fa_IR",  # Persian (Iran)
        # Note: Limited Persian support, may need custom names
    ],
    NameCulture.TURKISH_ALTAIC: [
        "tr_TR",  # Turkish
        # Note: Very limited Altaic language support in faker
    ],
    NameCulture.INDIGENOUS_TRADITIONAL: [
        "en_US",  # English - many indigenous names use English patterns
        # Note: Faker has no indigenous name support
        # Will need custom implementation for authentic names
    ],
    NameCulture.HEBREW_JEWISH: [
        "he_IL",  # Hebrew (Israel)
        "en_US",  # English - for Ashkenazi/diaspora names
    ],
}

# Map each culture to appropriate nationalities
CULTURE_NATIONALITIES: dict[NameCulture, list[str]] = {
    NameCulture.EAST_ASIAN: [
        "China", "Japan", "South Korea", "Taiwan", "Hong Kong",
        "Singapore", "Malaysia",  # diaspora communities
    ],
    NameCulture.ARABIC_ISLAMIC: [
        "Saudi Arabia", "Egypt", "Turkey", "Iran", "Iraq", "Syria",
        "Jordan", "Lebanon", "Morocco", "Algeria", "Tunisia",
        "United Arab Emirates", "Kuwait", "Qatar", "Pakistan",
        "Bangladesh", "Indonesia", "Malaysia",  # Muslim majority countries
    ],
    NameCulture.SOUTH_ASIAN: [
        "India", "Pakistan", "Bangladesh", "Sri Lanka", "Nepal",
        "Bhutan", "Afghanistan",
    ],
    NameCulture.WESTERN_EUROPEAN: [
        "United States", "United Kingdom", "Germany", "France",
        "Italy", "Netherlands", "Sweden", "Norway", "Denmark",
        "Finland", "Belgium", "Switzerland", "Austria", "Ireland",
        "Canada", "Australia", "New Zealand",  # diaspora countries
    ],
    NameCulture.SUB_SAHARAN_AFRICAN: [
        "Nigeria", "Kenya", "South Africa", "Ghana", "Ethiopia",
        "Tanzania", "Uganda", "Zimbabwe", "Botswana", "Senegal",
        "Mali", "Burkina Faso", "Ivory Coast", "Cameroon",
        "Democratic Republic of the Congo", "Rwanda",
    ],
    NameCulture.SPANISH_PORTUGUESE: [
        "Mexico", "Spain", "Brazil", "Argentina", "Colombia",
        "Peru", "Chile", "Venezuela", "Ecuador", "Guatemala",
        "Cuba", "Dominican Republic", "Honduras", "Paraguay",
        "Bolivia", "El Salvador", "Nicaragua", "Costa Rica",
        "Panama", "Uruguay", "Puerto Rico", "Portugal",
    ],
    NameCulture.SOUTHEAST_ASIAN: [
        "Thailand", "Indonesia", "Malaysia", "Philippines",
        "Vietnam", "Myanmar", "Cambodia", "Laos", "Singapore",
        "Brunei", "East Timor",
    ],
    NameCulture.SLAVIC_ORTHODOX: [
        "Russia", "Poland", "Czech Republic", "Slovakia",
        "Ukraine", "Belarus", "Bulgaria", "Serbia", "Croatia",
        "Slovenia", "Bosnia and Herzegovina", "Montenegro",
        "North Macedonia",
    ],
    NameCulture.IRANIAN_PERSIAN: [
        "Iran", "Afghanistan", "Tajikistan", "Uzbekistan",
        # Kurdish regions
        "Iraq", "Turkey", "Syria",
    ],
    NameCulture.TURKISH_ALTAIC: [
        "Turkey", "Kazakhstan", "Kyrgyzstan", "Turkmenistan",
        "Azerbaijan", "Mongolia",
    ],
    NameCulture.INDIGENOUS_TRADITIONAL: [
        "United States", "Canada", "Mexico", "Australia",
        "New Zealand", "Bolivia", "Peru", "Ecuador", "Guatemala",
        # Countries with significant indigenous populations
    ],
    NameCulture.HEBREW_JEWISH: [
        "Israel", "United States", "France", "United Kingdom",
        "Canada", "Argentina", "Russia", "Germany", "Australia",
        # Countries with significant Jewish diaspora populations
    ],
}

# Map each culture to appropriate cities for place_of_birth
CULTURE_CITIES: dict[NameCulture, list[str]] = {
    NameCulture.EAST_ASIAN: [
        "Beijing", "Shanghai", "Guangzhou", "Shenzhen",  # China
        "Tokyo", "Osaka", "Kyoto", "Yokohama",  # Japan
        "Seoul", "Busan", "Incheon",  # South Korea
        "Taipei", "Kaohsiung",  # Taiwan
        "Hong Kong", "Singapore",  # diaspora cities
    ],
    NameCulture.ARABIC_ISLAMIC: [
        "Cairo", "Alexandria",  # Egypt
        "Riyadh", "Jeddah", "Mecca",  # Saudi Arabia
        "Istanbul", "Ankara", "Izmir",  # Turkey
        "Tehran", "Isfahan", "Shiraz",  # Iran
        "Baghdad", "Basra",  # Iraq
        "Damascus", "Aleppo",  # Syria
        "Casablanca", "Rabat",  # Morocco
        "Karachi", "Lahore", "Islamabad",  # Pakistan
        "Dhaka", "Chittagong",  # Bangladesh
        "Jakarta", "Surabaya",  # Indonesia
    ],
    NameCulture.SOUTH_ASIAN: [
        "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
        "Kolkata", "Pune", "Ahmedabad", "Surat", "Jaipur",  # India
        "Karachi", "Lahore", "Faisalabad",  # Pakistan
        "Dhaka", "Chittagong",  # Bangladesh
        "Colombo", "Kandy",  # Sri Lanka
        "Kathmandu", "Pokhara",  # Nepal
    ],
    NameCulture.WESTERN_EUROPEAN: [
        "London", "Manchester", "Birmingham",  # UK
        "Berlin", "Munich", "Hamburg", "Cologne",  # Germany
        "Paris", "Lyon", "Marseille", "Toulouse",  # France
        "Rome", "Milan", "Naples", "Turin",  # Italy
        "Amsterdam", "Rotterdam", "The Hague",  # Netherlands
        "Stockholm", "Gothenburg", "Malmö",  # Sweden
        "Oslo", "Bergen", "Trondheim",  # Norway
        "Copenhagen", "Aarhus", "Odense",  # Denmark
        "New York", "Los Angeles", "Chicago", "Houston",  # US diaspora
        "Toronto", "Vancouver", "Montreal",  # Canada diaspora
    ],
    NameCulture.SUB_SAHARAN_AFRICAN: [
        "Lagos", "Abuja", "Kano", "Ibadan",  # Nigeria
        "Nairobi", "Mombasa", "Kisumu",  # Kenya
        "Cape Town", "Johannesburg", "Durban", "Pretoria",  # South Africa
        "Accra", "Kumasi",  # Ghana
        "Addis Ababa", "Dire Dawa",  # Ethiopia
        "Dar es Salaam", "Dodoma",  # Tanzania
        "Kampala", "Entebbe",  # Uganda
        "Dakar", "Saint-Louis",  # Senegal
    ],
    NameCulture.SPANISH_PORTUGUESE: [
        "Mexico City", "Guadalajara", "Monterrey", "Puebla",  # Mexico
        "Madrid", "Barcelona", "Valencia", "Seville",  # Spain
        "São Paulo", "Rio de Janeiro", "Salvador", "Brasília",  # Brazil
        "Buenos Aires", "Córdoba", "Rosario",  # Argentina
        "Bogotá", "Medellín", "Cali",  # Colombia
        "Lima", "Arequipa", "Trujillo",  # Peru
        "Santiago", "Valparaíso", "Concepción",  # Chile
        "Caracas", "Maracaibo", "Valencia",  # Venezuela
    ],
    NameCulture.SOUTHEAST_ASIAN: [
        "Bangkok", "Chiang Mai", "Phuket",  # Thailand
        "Jakarta", "Surabaya", "Bandung", "Medan",  # Indonesia
        "Kuala Lumpur", "George Town", "Johor Bahru",  # Malaysia
        "Manila", "Quezon City", "Cebu City",  # Philippines
        "Ho Chi Minh City", "Hanoi", "Da Nang",  # Vietnam
        "Yangon", "Mandalay",  # Myanmar
        "Phnom Penh", "Siem Reap",  # Cambodia
        "Singapore",  # Singapore
    ],
    NameCulture.SLAVIC_ORTHODOX: [
        "Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg",  # Russia
        "Warsaw", "Kraków", "Łódź", "Wrocław",  # Poland
        "Prague", "Brno", "Ostrava",  # Czech Republic
        "Bratislava", "Košice",  # Slovakia
        "Kiev", "Kharkiv", "Odessa",  # Ukraine
        "Minsk", "Gomel", "Vitebsk",  # Belarus
        "Sofia", "Plovdiv", "Varna",  # Bulgaria
        "Belgrade", "Novi Sad", "Niš",  # Serbia
        "Zagreb", "Split", "Rijeka",  # Croatia
    ],
    NameCulture.IRANIAN_PERSIAN: [
        "Tehran", "Mashhad", "Isfahan", "Karaj", "Shiraz",  # Iran
        "Kabul", "Kandahar", "Herat",  # Afghanistan
        "Dushanbe", "Khujand",  # Tajikistan
        "Erbil", "Sulaymaniyah",  # Kurdish regions
    ],
    NameCulture.TURKISH_ALTAIC: [
        "Istanbul", "Ankara", "Izmir", "Bursa", "Adana",  # Turkey
        "Almaty", "Nur-Sultan", "Shymkent",  # Kazakhstan
        "Bishkek", "Osh",  # Kyrgyzstan
        "Ashgabat", "Turkmenbashi",  # Turkmenistan
        "Baku", "Ganja",  # Azerbaijan
        "Ulaanbaatar", "Erdenet",  # Mongolia
    ],
    NameCulture.INDIGENOUS_TRADITIONAL: [
        # Note: These represent general regions, not specific indigenous communities
        "Anchorage", "Fairbanks",  # Alaska Native
        "Phoenix", "Albuquerque", "Flagstaff",  # Native American Southwest
        "Oklahoma City", "Tulsa",  # Native American Great Plains
        "La Paz", "Sucre",  # Bolivia Indigenous
        "Quito", "Cuenca",  # Ecuador Indigenous
        "Cusco", "Arequipa",  # Peru Indigenous
        "Guatemala City", "Quetzaltenango",  # Guatemala Indigenous
    ],
    NameCulture.HEBREW_JEWISH: [
        "Jerusalem", "Tel Aviv", "Haifa", "Beersheba",  # Israel
        "New York", "Los Angeles", "Miami", "Chicago",  # US diaspora
        "Paris", "Marseille", "Lyon",  # France diaspora
        "London", "Manchester", "Leeds",  # UK diaspora
        "Toronto", "Montreal", "Vancouver",  # Canada diaspora
        "Buenos Aires", "Córdoba",  # Argentina diaspora
        "Moscow", "Saint Petersburg",  # Russia diaspora
    ],
}


def get_random_locale(culture: NameCulture) -> str:
    """Get a random faker locale for the given culture."""
    import random
    locales = CULTURE_LOCALES.get(culture, ["en_US"])
    return random.choice(locales)


def get_random_nationality(culture: NameCulture) -> str:
    """Get a random nationality for the given culture."""
    import random
    nationalities = CULTURE_NATIONALITIES.get(culture, ["United States"])
    return random.choice(nationalities)


def get_random_city(culture: NameCulture) -> str:
    """Get a random city for the given culture."""
    import random
    cities = CULTURE_CITIES.get(culture, ["New York"])
    return random.choice(cities)
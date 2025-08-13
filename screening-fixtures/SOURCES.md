# Cultural Name Data Sources

This document identifies potential sources for obtaining culturally diverse name data to support the generation of realistic synthetic person records across different global naming conventions.

## Primary Libraries and Packages

### Python Faker Library
- **Package**: `faker`
- **Coverage**: Extensive locale support (80+ locales)
- **Strengths**: Well-maintained, standardized API, built-in city/country data, gender-aware name generation
- **Notable locales**: `en_US`, `es_ES`, `zh_CN`, `ja_JP`, `ar_SA`, `hi_IN`, `ru_RU`, `de_DE`, `fr_FR`, `pt_BR`, `ko_KR`, `th_TH`, `vi_VN`, `pl_PL`, `tr_TR`, `it_IT`, `nl_NL`, `sv_SE`, `no_NO`, `da_DK`, `fi_FI`, `cs_CZ`, `hu_HU`, `ro_RO`, `bg_BG`, `hr_HR`, `sk_SK`, `sl_SI`, `et_EE`, `lv_LV`, `lt_LT`
- **Usage**: Primary source for most name generation

### Names Dataset
- **Source**: `names-dataset` Python package
- **Coverage**: First names from 79 countries, surnames from 89 countries
- **Strengths**: Frequency data, gender information, country-specific data
- **Data**: Based on government census and official records

## Regional Name Sources

### Western European
- **English**: UK ONS (Office for National Statistics) popular names
- **German**: Gesellschaft für deutsche Sprache annual lists
- **French**: INSEE (Institut national de la statistique) name data
- **Spanish**: INE (Instituto Nacional de Estadística) name statistics
- **Italian**: ISTAT (Istituto nazionale di statistica) name data
- **Dutch**: CBS (Centraal Bureau voor de Statistiek) name statistics

### Slavic
- **Russian**: Rosstat official name statistics
- **Polish**: GUS (Główny Urząd Statystyczny) name data
- **Czech**: Czech Statistical Office name records
- **Ukrainian**: State Statistics Service name data
- **Serbian/Croatian**: Statistical offices of respective countries

### East Asian
- **Chinese**: 
  - Mainland: National Bureau of Statistics name data
  - Hong Kong: Immigration Department common names
  - Taiwan: Ministry of the Interior name statistics
- **Japanese**: Ministry of Health, Labour and Welfare name rankings
- **Korean**: Statistics Korea name data

### Southeast Asian
- **Thai**: Royal Institute of Thailand name guidelines
- **Vietnamese**: General Statistics Office name data
- **Indonesian**: Central Statistics Agency (BPS) name information
- **Malaysian**: Department of Statistics Malaysia name data
- **Filipino**: Philippine Statistics Authority name records

### South Asian
- **Indian**: 
  - Hindi/Sanskrit names from cultural databases
  - Regional variations (Tamil, Telugu, Bengali, Gujarati, Punjabi, etc.)
- **Pakistani**: Pakistan Bureau of Statistics name data
- **Bangladeshi**: Bangladesh Bureau of Statistics name information

### Middle Eastern and North African
- **Arabic**: Various statistical offices across MENA region
- **Persian**: Statistical Center of Iran name data
- **Turkish**: Turkish Statistical Institute name information
- **Hebrew**: Israel Central Bureau of Statistics name data

### Sub-Saharan African
- **Nigerian**: National Bureau of Statistics name information
- **Kenyan**: Kenya National Bureau of Statistics name data
- **South African**: Statistics South Africa name records
- **Ethiopian**: Central Statistical Agency name information
- **Ghanaian**: Ghana Statistical Service name data

### Nordic
- **Swedish**: Statistics Sweden name data
- **Norwegian**: Statistics Norway name information
- **Danish**: Statistics Denmark name records
- **Finnish**: Statistics Finland name data
- **Icelandic**: Statistics Iceland name information

## Geographic Data Sources

### Cities and Places of Birth
- **GeoNames**: Comprehensive global geographic database
- **World Cities Database**: Major cities worldwide with population data
- **Natural Earth**: Public domain map dataset with city information
- **OpenStreetMap**: Nominatim API for place name data

### Country and Nationality Data
- **ISO 3166**: Official country codes and names
- **UN Statistics**: Official country and territory names
- **CIA World Factbook**: Country information and demographics

## Specialized Cultural Resources

### Academic Sources
- **Unicode Common Locale Data Repository (CLDR)**: Standardized locale data
- **Ethnologue**: Comprehensive language and cultural information
- **World Atlas of Language Structures**: Linguistic and cultural data

### Government Statistical Offices
- Most countries maintain official name statistics through their national statistical offices
- Birth registration data often includes popular name trends
- Census data provides historical name usage patterns

## Data Quality Considerations

### Name Frequency
- Prioritize sources that include frequency or popularity data
- Avoid overly rare or archaic names that might seem unrealistic
- Balance common names with reasonable diversity

### Transliteration Standards
- Use consistent romanization systems (e.g., Pinyin for Chinese, Hepburn for Japanese)
- Consider multiple transliteration variants for the same name
- Account for different spelling conventions in diaspora communities

### Cultural Authenticity
- Ensure name combinations are culturally appropriate
- Respect naming conventions (family name order, patronymics, etc.)
- Consider generational naming patterns and trends

### Legal and Ethical Considerations
- Use only publicly available demographic data
- Avoid using real person directories or private databases
- Respect cultural sensitivity around sacred or ceremonial names
- Ensure compliance with data protection regulations

## Implementation Strategy

### Primary Approach
1. Use `faker` library as the foundation for most locales
2. Supplement with `names-dataset` for additional diversity
3. Create custom name lists for underrepresented cultures

### Secondary Sources
1. Scrape official statistical office data where publicly available
2. Use GeoNames for city/country correlation
3. Implement cultural fuzzing rules based on migration patterns

### Validation
1. Cross-reference generated names against multiple sources
2. Implement cultural consistency checks
3. Test for realistic name-geography correlations
4. Verify gender-name consistency across cultures

## Gender-Aware Name Generation

### Gender Classification Sources
- **Behind the Name**: Comprehensive database with gender associations for names across cultures
- **Gender Guesser**: Python library for predicting gender from names
- **Social Security Administration**: US name-gender statistics
- **National statistical offices**: Many countries provide gender breakdowns in name data

### Cultural Gender Considerations
- **Unisex names**: Some names are commonly used for multiple genders
- **Cultural variations**: Same name may have different gender associations across cultures
- **Modern trends**: Increasing use of gender-neutral names
- **Non-binary representation**: Include "other" category for realistic diversity

### Implementation Strategy for Gender
1. Use faker's built-in gender methods (`fake.first_name_male()`, `fake.first_name_female()`)
2. Cross-reference with names-dataset gender classifications
3. Implement probability-based gender assignment (~45% female, 45% male, 10% other)
4. Ensure cultural consistency between name choice and gender assignment
5. Handle gender-neutral names appropriately across different cultures
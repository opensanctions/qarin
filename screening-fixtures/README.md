# Screening Fixtures

A Python project that generates synthetic person records for testing sanctions and AML screening APIs. This tool creates realistic, diverse datasets to evaluate false-positive rates in financial compliance systems.

## Overview

This project generates compelling-looking synthetic person records that reflect diverse global name cultures, including Western European, Slavic, African, Chinese, Japanese, Thai, Indonesian, and others. The generated data simulates real-world customer databases used by insurance and financial services companies for compliance testing.

## Features

- **Multi-cultural name generation**: Supports diverse naming conventions from various cultures
- **Realistic data fuzzing**: Applies real-world data inconsistencies and cultural variations
- **Age-appropriate records**: Generates persons between 18-85 years old
- **Geographic correlation**: Matches place of birth and nationality to name cultures
- **CSV output**: Produces structured data suitable for API testing

## Output Format

The tool generates a CSV file with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `full_name` | Complete name of the person | "María Elena García López" |
| `first_name` | Given name | "María" |
| `middle_name` | Middle name (if present) | "Elena" |
| `last_name` | Family/surname | "García López" |
| `gender` | Gender (female, male, other) | "female" |
| `date_of_birth` | ISO date (18-85 years old) | "1987-03-15" |
| `place_of_birth` | City matching name culture | "Barcelona" |
| `nationality` | Country matching name culture | "Spain" |

## Data Fuzzing

The generated data includes realistic inconsistencies to simulate real-world scenarios:

- **Cultural mixing**: US citizens with various international name origins
- **Geographic dispersion**: People living outside their cultural origin countries  
- **Missing data**: ~10% probability of empty fields (except `full_name`)
- **Name variations**: Different naming conventions (some cultures don't use middle names or family names)

## Technical Requirements

- **Language**: Python with strict typing
- **Code quality**: Passes `ruff` linting and `mypy --strict` checks
- **Dependencies**: Managed with `uv`
- **Libraries**: Uses `faker` for name generation

## Installation

```bash
# Install dependencies
uv install

# Install development dependencies
uv install --dev
```

## Usage

```bash
# Generate synthetic data
python -m screening_fixtures

# Generate specific number of records
python -m screening_fixtures --count 10000

# Specify output file
python -m screening_fixtures --output customers.csv
```

## Development

### Code Quality

```bash
# Run linting
ruff check .

# Run type checking
mypy --strict .

# Format code
ruff format .
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=screening_fixtures
```

## Use Cases

- **API Testing**: Evaluate screening system false-positive rates
- **Performance Testing**: Generate large datasets for load testing
- **Compliance Testing**: Validate AML/sanctions screening accuracy
- **Development**: Provide realistic test data for financial services applications

## Contributing

1. Ensure code passes `ruff` and `mypy --strict`
2. Add tests for new functionality
3. Update documentation as needed

## License

[Add appropriate license information]

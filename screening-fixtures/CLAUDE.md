This Python project will generate a list of person names suitable for testing a screening API used
in sanctions and AML checks. The API's goal is produce a low false-positive rate, ie. when the name of 
a person that is not subject to sanctions is submitted, it should not trigger an alert. This codebase
will merely generate a testing dataset of synthetic, normal-looking person records which can be used
to simulate a use of the screening API against a database such as a customer list of an insurance or
financial services company. The goal is to generate compelling-looking entries that reflect a diversity
of name cultures (Western European, Slavic, African, Chinese, Japanese, Thai, Indionesian, etc.)

## Desired output

The goal is to generate a synthetic CSV file, with the following columns:

* `full_name` - the full name of the person
* `first_name` - the first name present in the full name
* `middle_name` - a middle name, if present
* `last_name` - the last or family name of the person
* `gender` - gender (female, male, other) that matches the name culturally
* `date_of_birth` - an ISO date, which makes the person between 18 and 85 years old at the time of data generation
* `place_of_birth` - ideally, a name of a city that corresponds to the name culture of the main name
* `nationality` - a country name, that corresponds to the name culture of the main name

## Fuzzing

For all of the data generated, errors should be applied to reflect real world shifts in data and culture.
For example, US citizens can carry a wide variety of name cultures, and many people live outside the country that
is native to the culture from which their name stems. 
Many people may not have a middle name, or the concept of a family name may not apply to their name culture.
All feels, other than full name, should be empty with a certain probability (say, 10%)

## LLM-Assisted Generation with Quality Control

While libraries like `faker` provide good baseline name generation, LLMs can offer superior cultural authenticity and diversity. However, LLMs are prone to quality degradation over extended sessions. Here's a proposed approach:

### Hybrid Generation Strategy

1. **Primary Sources**: Use `faker` and `names-dataset` as foundational generators
2. **LLM Enhancement**: Use Claude API for culturally nuanced names that traditional libraries miss
3. **Quality Control**: Implement multiple validation layers to prevent LLM drift

### Batch-Based LLM Generation

* **Small batches**: Generate 25-50 records per LLM session to prevent quality degradation
* **Fresh sessions**: Start new API conversations for each batch to avoid context drift
* **Cultural focus**: Each batch targets specific cultural/regional combinations
* **Templated prompts**: Use consistent, well-tested prompts for each cultural context

### Quality Control Pipeline

1. **Pre-validation**: Check names against cultural databases from SOURCES.md
2. **Cross-validation**: Verify gender-name consistency using `gender-guesser` or similar
3. **Geographic validation**: Ensure place_of_birth and nationality align with name culture
4. **Duplicate detection**: Prevent identical or near-identical records
5. **Realism scoring**: Flag overly exotic or suspicious combinations

### LLM Session Management

```python
# Example approach
def generate_cultural_batch(culture: str, count: int = 25) -> List[PersonRecord]:
    """Generate a small batch focused on one culture to maintain quality"""
    prompt = get_cultural_prompt(culture)
    response = claude_api.call(prompt, max_tokens=2000)
    records = parse_llm_response(response)
    
    # Quality control
    validated_records = []
    for record in records:
        if validate_cultural_consistency(record, culture):
            validated_records.append(record)
    
    return validated_records
```

### Fallback Strategy

If LLM-generated records fail validation:
1. Fall back to `faker` for that cultural group
2. Log the failure for prompt refinement
3. Continue with next batch to avoid session contamination

### Validation Rules

* **Name plausibility**: Cross-check against Behind the Name database
* **Cultural consistency**: Verify name-nationality-place combinations
* **Gender alignment**: Ensure names match assigned gender in target culture
* **Format compliance**: Validate all required fields are properly formatted
* **Uniqueness**: Prevent duplicate full names within dataset

## Tech

* We're building everything in a Python package called `namegen`. 
* Write typed python Python code that passes `ruff` linting and `mypy --strict`
* Use `uv` for dependency management
* Use absolute imports throughout the codebase (e.g., `from namegen.models import PersonRecord`) 
* API credentials are stored in a `.envrc` file read by autoenv.
* Primary libraries: `faker`, `names-dataset`, `anthropic` (Claude API)
* Validation libraries: `gender-guesser`, custom cultural validators
* The python package exposes a `click` CLI command called `namegen` (in `namegen/cli.py`)
* The command `namegen generate -l <lines> <screening.csv>` will produce an output file
* The command `namegen validate <screening.csv>` will add two columns to the file: one to assign a plausibility `score` to each generated persona, and one called `skip` if the score is below a threshold.
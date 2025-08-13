"""Command-line interface for namegen."""

import csv
import os
from pathlib import Path

import click

from namegen.generators import generate_records
from namegen.validators import RecordValidator
from namegen.cultures import NameCulture


@click.group()
@click.version_option()
def cli() -> None:
    """Generate synthetic person records for screening API testing."""
    pass


@cli.command()
@click.option(
    "-l", "--lines",
    type=int,
    default=1000,
    help="Number of records to generate (default: 1000)"
)
@click.option(
    "--seed",
    type=int,
    help="Random seed for reproducible generation"
)
@click.option(
    "--culture",
    type=click.Choice([c.value for c in NameCulture], case_sensitive=False),
    help="Generate records from single culture (overrides --distribution)"
)
@click.option(
    "--distribution",
    type=click.Choice(["global", "us"], case_sensitive=False),
    default="global",
    help="Use global or US demographic distribution (default: global)"
)
@click.argument("output_file", type=click.Path())
def generate(lines: int, seed: int | None, culture: str | None, distribution: str, output_file: str) -> None:
    """Generate synthetic person records and save to CSV file."""

    # Use seed from parameter, environment, or none
    if seed is None:
        seed_str = os.getenv("NAMEGEN_SEED")
        if seed_str:
            try:
                seed = int(seed_str)
            except ValueError:
                click.echo(f"Warning: Invalid NAMEGEN_SEED '{seed_str}', ignoring", err=True)

    click.echo(f"Generating {lines} records...")
    if seed is not None:
        click.echo(f"Using random seed: {seed}")

    # Parse culture if provided
    target_culture = None
    if culture:
        target_culture = NameCulture(culture)
        click.echo(f"Generating records from culture: {culture}")
    else:
        click.echo(f"Using {distribution} distribution")
    
    # Generate records
    records = generate_records(lines, seed=seed, culture=target_culture, distribution=distribution)

    # Write to CSV
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'full_name', 'first_name', 'middle_name', 'last_name',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:
            writer.writerow(record.to_dict())

    click.echo(f"Generated {len(records)} records to {output_file}")


@cli.command()
@click.option(
    "--threshold",
    type=float,
    default=0.7,
    help="Quality threshold below which records are marked to skip (default: 0.7)"
)
@click.argument("csv_file", type=click.Path(exists=True))
def validate(threshold: float, csv_file: str) -> None:
    """Validate existing CSV file and add quality scores."""

    csv_path = Path(csv_file)

    if not csv_path.exists():
        click.echo(f"Error: File {csv_file} does not exist", err=True)
        return

    click.echo(f"Validating records in {csv_file}...")
    click.echo(f"Using quality threshold: {threshold}")

    validator = RecordValidator()

    try:
        validator.validate_csv_file(csv_path, threshold=threshold)
        click.echo("Validation complete. Added 'score' and 'skip' columns.")
    except Exception as e:
        click.echo(f"Error validating file: {e}", err=True)


if __name__ == "__main__":
    cli()

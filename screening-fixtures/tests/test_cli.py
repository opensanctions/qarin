"""Tests for namegen CLI."""

import csv
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from namegen.cli import cli


@pytest.fixture
def runner():
    """Create a Click test runner."""
    return CliRunner()


def test_cli_help(runner):
    """Test CLI help message."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Generate synthetic person records' in result.output


def test_generate_command_help(runner):
    """Test generate command help."""
    result = runner.invoke(cli, ['generate', '--help'])
    assert result.exit_code == 0
    assert 'Generate synthetic person records and save to CSV' in result.output


def test_validate_command_help(runner):
    """Test validate command help."""
    result = runner.invoke(cli, ['validate', '--help'])
    assert result.exit_code == 0
    assert 'Validate existing CSV file' in result.output


def test_generate_basic(runner):
    """Test basic generate command."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_output.csv"

        result = runner.invoke(cli, [
            'generate',
            '-l', '5',
            str(output_file)
        ])

        assert result.exit_code == 0
        assert 'Generating 5 records' in result.output
        assert 'Generated 5 records' in result.output

        # Check file was created and has correct structure
        assert output_file.exists()

        with open(output_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 5

        # Check headers
        expected_headers = [
            'full_name', 'first_name', 'middle_name', 'last_name',
            'gender', 'date_of_birth', 'place_of_birth', 'nationality'
        ]
        assert list(reader.fieldnames) == expected_headers

        # Check first row has data
        first_row = rows[0]
        assert first_row['full_name']
        assert first_row['first_name']
        assert first_row['gender'] in ['female', 'male', 'other']


def test_generate_with_seed(runner):
    """Test generate command with seed for reproducibility."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file1 = Path(tmpdir) / "test1.csv"
        output_file2 = Path(tmpdir) / "test2.csv"

        # Generate with same seed twice
        result1 = runner.invoke(cli, [
            'generate', '--seed', '42', '-l', '3',
            str(output_file1)
        ])
        result2 = runner.invoke(cli, [
            'generate', '--seed', '42', '-l', '3',
            str(output_file2)
        ])

        assert result1.exit_code == 0
        assert result2.exit_code == 0

        # Read both files
        with open(output_file1, newline='', encoding='utf-8') as f:
            rows1 = list(csv.DictReader(f))

        with open(output_file2, newline='', encoding='utf-8') as f:
            rows2 = list(csv.DictReader(f))

        # Should be identical
        assert len(rows1) == len(rows2) == 3
        for i in range(3):
            assert rows1[i]['full_name'] == rows2[i]['full_name']


def test_generate_with_env_seed(runner):
    """Test generate command with seed from environment."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "test_env.csv"

        # Set environment variable
        env = {'NAMEGEN_SEED': '123'}

        result = runner.invoke(cli, [
            'generate', '-l', '2',
            str(output_file)
        ], env=env)

        assert result.exit_code == 0
        assert 'Using random seed: 123' in result.output


def test_validate_basic(runner):
    """Test basic validate command."""
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "test_validate.csv"

        # Create test CSV
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'full_name', 'first_name', 'middle_name', 'last_name',
                'gender', 'date_of_birth', 'place_of_birth', 'nationality'
            ])
            writer.writerow([
                'John Doe', 'John', '', 'Doe',
                'male', '1990-01-01', 'New York', 'United States'
            ])

        result = runner.invoke(cli, ['validate', str(csv_file)])

        assert result.exit_code == 0
        assert f'Validating records in {csv_file}' in result.output
        assert 'Validation complete' in result.output

        # Check that score and skip columns were added
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert 'score' in reader.fieldnames
        assert 'skip' in reader.fieldnames
        assert len(rows) == 1


def test_validate_with_custom_threshold(runner):
    """Test validate command with custom threshold."""
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = Path(tmpdir) / "test_threshold.csv"

        # Create test CSV with questionable data
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'full_name', 'first_name', 'middle_name', 'last_name',
                'gender', 'date_of_birth', 'place_of_birth', 'nationality'
            ])
            writer.writerow([
                'Bad Record', 'Wrong', '', 'Names',
                'invalid', '1990-01-01', 'City', 'Country'
            ])

        result = runner.invoke(cli, [
            'validate', '--threshold', '0.5', str(csv_file)
        ])

        assert result.exit_code == 0
        assert 'Using quality threshold: 0.5' in result.output


def test_validate_nonexistent_file(runner):
    """Test validate command with non-existent file."""
    result = runner.invoke(cli, ['validate', '/nonexistent/file.csv'])

    assert result.exit_code == 2  # Click exits with 2 for bad parameter
    assert 'does not exist' in result.output


def test_generate_creates_directories(runner):
    """Test that generate command creates parent directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        nested_path = Path(tmpdir) / "nested" / "directory" / "output.csv"

        result = runner.invoke(cli, [
            'generate', '-l', '1', str(nested_path)
        ])

        assert result.exit_code == 0
        assert nested_path.exists()
        assert nested_path.parent.exists()

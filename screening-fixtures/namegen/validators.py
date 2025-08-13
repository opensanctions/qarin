"""Validation utilities for generated person records."""

import csv
from pathlib import Path

from namegen.models import PersonRecord


class RecordValidator:
    """Validates the quality and plausibility of generated records."""

    def validate_record(self, record: PersonRecord) -> float:
        """
        Validate a single record and return plausibility score (0.0-1.0).

        Higher scores indicate more plausible/realistic records.
        """
        score = 1.0

        # Basic format checks
        if not record.full_name.strip():
            score -= 0.5

        if not record.first_name.strip():
            score -= 0.3

        if not record.last_name.strip():
            score -= 0.3

        # Gender validation
        if record.gender not in ["female", "male", "other"]:
            score -= 0.2

        # Name consistency checks
        if record.first_name not in record.full_name:
            score -= 0.3

        if record.last_name not in record.full_name:
            score -= 0.3

        # Age validation (should be 18-85)
        from datetime import date
        age_days = (date.today() - record.date_of_birth).days
        age_years = age_days / 365.25

        if age_years < 18 or age_years > 85:
            score -= 0.4

        return max(0.0, score)

    def validate_csv_file(self, csv_path: Path, threshold: float = 0.7) -> None:
        """
        Add validation columns to existing CSV file.

        Adds 'score' and 'skip' columns based on plausibility analysis.
        """
        # Read existing data
        rows = []
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            if not fieldnames:
                raise ValueError("CSV file has no headers")

            for row in reader:
                rows.append(row)

        # Add validation columns
        new_fieldnames = list(fieldnames) + ['score', 'skip']

        # Process each row
        for row in rows:
            try:
                # Convert row to PersonRecord for validation
                from datetime import date
                record = PersonRecord(
                    full_name=row.get('full_name', ''),
                    first_name=row.get('first_name', ''),
                    middle_name=row.get('middle_name') or None,
                    last_name=row.get('last_name', ''),
                    gender=row.get('gender', ''),
                    date_of_birth=date.fromisoformat(row.get('date_of_birth', '')),
                    place_of_birth=row.get('place_of_birth', ''),
                    nationality=row.get('nationality', ''),
                )

                score = self.validate_record(record)
                row['score'] = f"{score:.2f}"
                row['skip'] = "true" if score < threshold else "false"

            except Exception:
                # If validation fails, mark as low score
                row['score'] = "0.00"
                row['skip'] = "true"

        # Write updated CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=new_fieldnames)
            writer.writeheader()
            writer.writerows(rows)

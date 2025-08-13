"""Data models for person records."""

from dataclasses import dataclass
from datetime import date


@dataclass
class PersonRecord:
    """Represents a synthetic person record for screening tests."""

    full_name: str
    first_name: str
    middle_name: str | None
    last_name: str
    gender: str  # "female", "male", "other"
    date_of_birth: date
    place_of_birth: str
    nationality: str

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary for CSV export."""
        return {
            "full_name": self.full_name,
            "first_name": self.first_name,
            "middle_name": self.middle_name or "",
            "last_name": self.last_name,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth.isoformat(),
            "place_of_birth": self.place_of_birth,
            "nationality": self.nationality,
        }

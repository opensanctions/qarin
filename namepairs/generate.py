import csv
import orjson
import logging
from pathlib import Path
from typing import Dict, Set, Tuple
from itertools import combinations
from followthemoney import model
from followthemoney.types import registry
from nomenklatura.stream import StreamEntity as Entity
from nomenklatura.util import bool_text

log = logging.getLogger("genpairs")

STATEMENTS_PATH = Path("/Users/pudo/Data/statements.csv")
SCHEMATA = ("Organization", "Person", "Company", "PublicBody")
HEADERS = ["left", "right", "match", "type"]
DEDUPED_DATASETS = set(
    [
        "eu_fsf",
        "us_ofac_sdn",
        "gb_hmt_sanctions",
        "wikidata",
        "ext_gleif",
    ]
)


class Name:
    """A typed name of an entity."""

    __slots__ = ["name", "lang"]

    def __init__(self, name: str, lang: str):
        self.name = name
        self.lang = lang

    def __hash__(self) -> int:
        return hash((self.name, self.lang))

    def __eq__(self, other: "Name") -> bool:
        return self.name == other.name and self.lang == other.lang

    def __repr__(self) -> str:
        return f"{self.name} ({self.lang})"

    def __str__(self) -> str:
        return self.name


ENTITY_TYPES: Dict[str, str] = {}
ENTITY_NAMES: Dict[str, Set[Name]] = {}
ENTITY_DATASETS: Dict[str, Set[str]] = {}
NAME_TYPES: Dict[str, str] = {}


def load_entities():
    log.info("Loading entities: %s..." % STATEMENTS_PATH.as_posix())
    name_count = 0
    with open(STATEMENTS_PATH, "r") as fh:
        for row in csv.DictReader(fh):
            if row["schema"] not in SCHEMATA:
                continue
            if row["prop_type"] != "name":
                continue
            type = "PER" if row["schema"] == "Person" else "ORG"
            canonical_id = row["canonical_id"]
            schema = model.get(row["schema"])
            if schema is None:
                continue
            prop = schema.get(row["prop"])
            if prop is None or not prop.matchable:
                continue

            name = row["value"]
            if type == "PER":
                if "/" in name or "(" in name:
                    continue
            if " " not in name:
                continue
            if len(name) < 4:
                continue
            # if name in NAME_TYPES and NAME_TYPES[name] != type:
            #     NAME_TYPES[name] = "ANY"
            # else:
            #     NAME_TYPES[name] = type
            # if len(names) == 0:
            #     continue
            name_obj = Name(name, row["lang"])
            name_count += 1
            ENTITY_TYPES[canonical_id] = type
            if canonical_id not in ENTITY_DATASETS:
                ENTITY_DATASETS[canonical_id] = set()
            ENTITY_DATASETS[canonical_id].add(row["dataset"])
            if canonical_id not in ENTITY_NAMES:
                ENTITY_NAMES[canonical_id] = set()
            ENTITY_NAMES[canonical_id].add(name_obj)

    log.info("Loaded %s entities with %s names.", len(ENTITY_NAMES), name_count)


def generate_pairs():
    pairs: Dict[Tuple[str, str], bool] = {}

    for names in ENTITY_NAMES.values():
        for left, right in combinations(names, 2):
            if left == right:
                continue
            if left > right:
                left, right = right, left
            pairs[(left, right)] = True
    match_pairs = len(pairs)
    log.info("Generated %s matching pairs.", match_pairs)

    entity_ids = list(ENTITY_TYPES.keys())
    for left, right in combinations(entity_ids, 2):
        if ENTITY_TYPES[left] != ENTITY_TYPES[right]:
            continue
        if left > right:
            continue
        common_ds = ENTITY_DATASETS[left].intersection(ENTITY_DATASETS[right])
        if len(common_ds.intersection(DEDUPED_DATASETS)) == 0:
            continue

        left_names = ENTITY_NAMES[left]
        right_names = ENTITY_NAMES[right]
        if len(left_names.intersection(right_names)) > 0:
            continue
        # TODO: decide better which ones to choose:
        for left_name, right_name in zip(left_names, right_names):
            if left_name > right_name:
                left_name, right_name = right_name, left_name
            key = (left_name, right_name)
            if pairs.get(key) is True:
                pairs.pop(key)
                continue
            pairs[key] = False
            if len(pairs) % 100_000 == 0:
                log.info("Upd: %s non-matching pairs", len(pairs) - match_pairs)
            break
    log.info("Generated %s non-matching pairs.", len(pairs) - match_pairs)

    for (left, right), match in pairs.items():
        if NAME_TYPES[left] == "ANY" or NAME_TYPES[right] == "ANY":
            continue
        yield left, right, match, NAME_TYPES[left]


def write_csv():
    with open("pairs.csv", "w") as fh:
        writer = csv.writer(fh, dialect=csv.unix_dialect)
        writer.writerow(HEADERS)
        for left, right, match, type in generate_pairs():
            writer.writerow([left, right, bool_text(match), type])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_entities()
    write_csv()

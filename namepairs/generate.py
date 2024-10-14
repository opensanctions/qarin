import csv
import orjson
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple
from itertools import combinations
from followthemoney import model
from followthemoney.types import registry
from nomenklatura.stream import StreamEntity as Entity
from nomenklatura.util import bool_text

log = logging.getLogger("genpairs")

ENTITIES_PATH = Path("/Users/pudo/Downloads/default.json")
HEADERS = ["left", "right", "match", "type"]
DEDUPED_DATASETS = set(
    [
        "eu_fsf",
        "us_ofac_sdn",
        "ca_dfatd_sema_sanctions",
        "gb_hmt_sanctions",
        "ar_repet",
        "wikidata",
        "ext_gleif",
    ]
)

ENTITY_TYPES: Dict[str, str] = {}
ENTITY_NAMES: Dict[str, Set[str]] = {}
ENTITY_DATASETS: Dict[str, Set[str]] = {}
NAME_TYPES: Dict[str, str] = {}


def load_entities():
    log.info("Loading entities: %s..." % ENTITIES_PATH.as_posix())
    name_count = 0
    with open(ENTITIES_PATH, "rb") as fh:
        while line := fh.readline():
            obj = orjson.loads(line)
            entity = Entity.from_dict(model, obj)
            if not entity.schema.is_a("Organization") and not entity.schema.is_a(
                "Person"
            ):
                continue
            type = "ORG" if entity.schema.is_a("Organization") else "PER"

            names: Set[str] = set()
            for name in entity.get_type_values(registry.name, matchable=True):
                if type == "PER":
                    if "/" in name or "(" in name:
                        continue
                if " " not in name:
                    continue
                if len(name) < 4:
                    continue
                names.add(name)
                name_count += 1
                if name in NAME_TYPES and NAME_TYPES[name] != type:
                    NAME_TYPES[name] = "ANY"
                else:
                    NAME_TYPES[name] = type
            if len(names) == 0:
                continue
            ENTITY_TYPES[entity.id] = type
            ENTITY_DATASETS[entity.id] = entity.datasets
            ENTITY_NAMES[entity.id] = names

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

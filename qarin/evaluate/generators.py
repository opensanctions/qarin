from faker import Faker
from collections import OrderedDict
from followthemoney import model
import json
import random
from typing import List


def switch_random_character(s: str) -> str:
    """
    Switch two random characters in a string.
    Joe Biden -> Jeo Biden
    """
    if len(s) == 0:
        return s
    i = random.randint(1, len(s) - 1)
    return s[: i - 1] + s[i] + s[i - 1] + s[i + 1 :]


def second_name_last_name_first_names(s: str) -> str:
    """
    Switch the first and last names of a person, joining with a comma.
    Joe Biden -> Biden, Joe
    Pablo Ruiz Picasso -> Ruiz Picasso, Pablo
    """
    if len(s) == 0:
        return s
    names = s.split(" ")
    if len(names) < 2:
        return s
    return " ".join(names[1:]) + ", " + names[0]


def replace_spaces_with_special_char(s: str) -> str:
    """
    Replace all spaces with a non-breaking space.
    Pablo Picasso -> Pablo\u00a0Picasso
    """
    return s.replace(" ", " ")


def replace_non_ascii_with_special_char(s: str) -> str:
    """
    Replace all non-ascii characters with a special char.
    Schrödinger -> Schr?dinger
    """
    return "".join([c if ord(c) < 128 else "?" for c in s])


def replace_double_character_with_single(s: str) -> str:
    """
    Replace all double characters with a single character.
    Pablo Picasso -> Pablo Picaso
    """
    return "".join([c for i, c in enumerate(s) if i == 0 or s[i - 1] != c])


def remove_special_characters(s: str) -> str:
    """
    Remove all special characters.
    Schrödinger -> Schrdinger
    """
    return "".join([c if ord(c) < 128 else "" for c in s])


def duplicate_random_character(s: str) -> str:
    """
    Duplicate a random character in a string.
    Pablo Picasso -> Pabblo Picasso
    """
    if len(s) == 0:
        return s
    i = random.randint(0, len(s) - 1)
    return s[:i] + s[i] + s[i:]


def replace_random_vowel(s: str) -> str:
    """
    Replace a random vowel with another vowel.
    Pablo Picasso -> Pabla Picasso
    """
    vowels = "aeiouy"
    if len(s) == 0:
        return s
    i = random.randint(0, len(s) - 1)
    if s[i] in vowels:
        return s[:i] + random.choice(vowels) + s[i + 1 :]
    return s


def noop(s: str) -> str:
    return s


treatment_mapping = {
    "switch_random_character": switch_random_character,
    "second_name_last_name_first_names": second_name_last_name_first_names,
    "replace_spaces_with_special_char": replace_spaces_with_special_char,
    "replace_non_ascii_with_special_char": replace_non_ascii_with_special_char,
    "replace_double_character_with_single": replace_double_character_with_single,
    "remove_special_characters": remove_special_characters,
    "duplicate_random_character": duplicate_random_character,
    "replace_random_vowel": replace_random_vowel,
    "noop": noop,
}


class PersonGenerator:
    def __init__(self, locales: OrderedDict[str] = None):
        self.fake = Faker(locales)

    def generate(self, locale: str = None):
        """
        Generate a person with a random name.
        params:
            locale: str = None
                The locale to use for the properties."""
        entity = model.make_entity("Person")
        if locale is not None:
            fake = self.fake[locale]
        else:
            fake = self.fake
        entity.add("name", fake.name())

        entity.id = self.fake.uuid4()
        return entity

    def add_treatments(self, entity, treatments: List[str] = None):
        if treatments is None:
            treatments = list(treatment_mapping.keys())
        d = {}
        for treatment in treatments:
            changed = entity.clone()
            fn = treatment_mapping[treatment]
            changed.set("name", fn(entity.get("name")[0]))
            d[treatment] = changed
        return d

    def create_fixture_with_treatment(
        self, treatments: List[str] = None, locale: str = None
    ):
        if treatments is None:
            treatments = list(treatment_mapping.keys())
        d = {}
        original = self.generate(locale=locale)
        d["original"] = original
        d["locale"] = locale
        d["changed"] = self.add_treatments(original, treatments=treatments)
        return d


def create_fixtures_with_treatment(
    fname: str,
    n: int = 10,
    treatments: List[str] = None,
):
    if treatments is None:
        treatments = list(treatment_mapping.keys())
    for treatment in treatments:
        if treatment not in treatments:
            raise ValueError(f"Unknown treatment: {treatment}")
    with open(fname, mode="w") as f:
        persons = []
        for _ in range(0, n):
            d = {}
            person = PersonGenerator().generate()
            changed = person.clone()
            d["original"] = person.to_dict()
            d["changed"] = {}
            for treatment in treatments:
                fn = treatment_mapping[treatment]
                changed.set("name", fn(person.get("name")[0]))
                d["changed"][treatment] = changed.to_dict()
            persons.append(d)
        json.dump(persons, f)


def add_treatments(entity, n: int = 10, treatments: List[dict] = None):
    if treatments is None:
        treatments = list(treatment_mapping.keys())
    for treatment in treatments:
        if treatment not in treatments:
            raise ValueError(f"Unknown treatment: {treatment}")
    d = {}
    changed = entity.clone()
    d["original"] = entity.to_dict()
    d["changed"] = {}
    for treatment in treatments:
        fn = treatment_mapping[treatment]
        changed.set("name", fn(entity.get("name")[0]))
        d["changed"][treatment] = changed.to_dict()
    yield d

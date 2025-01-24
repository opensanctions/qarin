# import os
import duckdb
import logging
from pathlib import Path
from typing import Optional
from normality import latinize_text

# from rapidfuzz.distance import Levenshtein
from fingerprints import fingerprint
from fingerprints import clean_entity_prefix
from rigour.names.tokenize import tokenize_name
# from rigour.names.compare import align_name_parts
# from rigour.text.distance import levenshtein_similarity

STATEMENTS_PATH = Path("/Users/pudo/Data/statements.csv")
RESOLVER_PATH = Path("/Users/pudo/Code/operations/etl/data/resolve.ijson")
con = duckdb.connect("work.duckdb")
log = logging.getLogger("duck_gen")

score_count = 0
fp_count = 0


def load_statements():
    """Load the statements from the CSV file into the DuckDB."""
    log.info("Loading statements...")
    con.execute("DROP TABLE IF EXISTS statements;")
    con.execute(
        "CREATE TABLE statements AS SELECT * FROM read_csv(?, header=true);",
        [STATEMENTS_PATH.as_posix()],
    )


def load_resolver():
    """Load the resolver data into the DuckDB."""
    log.info("Loading resolver data...")
    con.execute("DROP TABLE IF EXISTS resolver;")
    con.execute(
        "CREATE TABLE resolver AS "
        "SELECT "
        "json->>0 AS left_id, "
        "json->>1 as right_id, "
        "json->>2 AS judgement, "
        'json->>4 AS "user" '
        "FROM read_json(?, format = 'newline_delimited');",
        [RESOLVER_PATH.as_posix()],
    )
    for _ in range(15):
        con.execute(
            "UPDATE resolver rx SET left_id = ry.left_id FROM resolver ry "
            "WHERE rx.left_id = ry.right_id AND ry.judgement = 'positive' AND rx.judgement <> 'positive';"
        )
        con.execute(
            "UPDATE resolver rx SET right_id = ry.left_id FROM resolver ry "
            "WHERE rx.right_id = ry.right_id AND ry.judgement = 'positive' AND rx.judgement <> 'positive';"
        )


def make_names_table():
    """Create a table of unique names from the statements."""
    log.info("Creating names table...")
    con.execute("DROP TABLE IF EXISTS names;")
    con.execute(
        "CREATE TABLE names AS "
        "SELECT canonical_id AS entity_id, schema, value AS name, lang, dataset "
        "FROM statements "
        "WHERE prop_type = 'name' AND prop <> 'weakAlias' AND "
        " schema IN ('Company', 'Organization', 'Person', 'PublicBody');"
    )
    con.execute("ALTER TABLE names ADD COLUMN category VARCHAR;")
    con.execute("UPDATE names SET category = IF(schema = 'Person', 'PER', 'ORG');")
    con.execute("ALTER TABLE names ADD COLUMN norm VARCHAR;")
    con.execute("ALTER TABLE names ADD COLUMN fp VARCHAR;")
    # Remove duplicate names:
    con.execute(
        "WITH ranked_names AS ( "
        "SELECT ROWID, ROW_NUMBER() OVER ( "
        "PARTITION BY name, entity_id "
        "ORDER BY lang DESC, ROWID "
        ") AS rn FROM names) "
        "DELETE FROM names "
        "WHERE ROWID IN (SELECT ROWID FROM ranked_names WHERE rn > 1);"
    )


def normalize_name(name: str, category: str) -> Optional[str]:
    """Normalize a name for comparison."""
    if name is None or len(name) < 4:
        return None
    name = name.lower()
    if category == "PER":
        if "/" in name or "(" in name or ")" in name:
            return None
        if " " not in name:
            return None
        # Remove prefixes like Mr., Mrs., etc.
        name = clean_entity_prefix(name)
    tokens = tokenize_name(name)
    if len(tokens) == 0:
        return None
    latins = (latinize_text(t) for t in tokens)
    norm = " ".join((p for p in latins if p is not None))
    # print(name, "->", norm)
    return norm


def fingerprint_name(name: str, category: str) -> Optional[str]:
    """Fingerprint a name for comparison."""
    global fp_count
    fp_count = fp_count + 1
    if fp_count > 0 and fp_count % 100_000 == 0:
        log.info("Fingerprinted %s names...", fp_count)
    return fingerprint(name)


# def ref_score(left: str, right: str) -> float:
#     global score_count
#     if left is None or right is None:
#         return 0.0
#     left = left.lower()
#     right = right.lower()
#     # base_distance = Levenshtein.distance(left, right)
#     # base_score = 1.0 - (base_distance / max(len(left), len(right)))

#     left_fp = fingerprint(left, keep_order=True)
#     right_fp = fingerprint(right, keep_order=True)
#     aligned = align_name_parts(left_fp.split(" "), right_fp.split(" "))
#     left_aligned = " ".join([a[0] for a in aligned if a[0] is not None])
#     right_aligned = " ".join([a[1] for a in aligned if a[1] is not None])
#     # print("XXXX", left, right, left_aligned, right_aligned)
#     al_distance = Levenshtein.distance(left_aligned, right_aligned)
#     al_score = 1.0 - (al_distance / max(len(left_aligned), len(right_aligned)))
#     score_count = score_count + 1
#     if score_count > 0 and score_count % 100_000 == 0:
#         log.info("Scored %s pairs...", score_count)
#     # return max(al_score, base_score)
#     return al_score


def generate_name_norms():
    """Generate a normalized version of the names."""
    log.info("Generate normalized names...")
    # con.execute("ALTER TABLE names DROP COLUMN norm IF EXISTS;")
    con.execute("UPDATE names SET norm = normalize_name(name, category);")
    # con.execute("ALTER TABLE names ADD COLUMN fp VARCHAR;")
    con.execute("UPDATE names SET fp = fingerprint_name(name, category);")


def compute_pairs():
    log.info("Computing positive pairs...")
    con.execute("DROP TABLE IF EXISTS pairs;")
    con.execute("""
        CREATE TABLE pairs AS
        SELECT nl.name AS left_name, nl.norm as left_norm, nl.fp AS left_fp, nl.lang AS left_lang, nl.category AS left_category,
               nr.name AS right_name, nr.norm as right_norm, nr.fp AS right_fp, nr.lang AS right_lang, nr.category AS right_category,
               true AS match, 0 AS dist_norm, 0 AS dist_fp, 0.0 AS score, nr.entity_id AS source
        FROM names nl, names nr
        WHERE nl.entity_id = nr.entity_id AND LOWER(nl.name) > LOWER(nr.name);
    """)
    # NB: Can filter on nl.norm <> nr.norm here.


def compute_non_pairs():
    log.info("Computing negatives pairs...")
    con.execute("DROP TABLE IF EXISTS non_pairs;")
    # Create a table of non-pairs from the resolver data:
    con.execute("""
        CREATE TABLE non_pairs AS 
        SELECT GREATEST(left_id, right_id) AS max_id, LEAST(left_id, right_id) AS min_id, judgement AS source 
        FROM resolver WHERE judgement IN ('unsure', 'negative');
    """)
    # Pick some wikidata comparisons by random:
    con.execute(
        "INSERT INTO non_pairs "
        "WITH entities AS (SELECT DISTINCT entity_id AS id FROM names WHERE STARTS_WITH(id, 'Q') USING SAMPLE 1000 ROWS) "
        "SELECT r.id AS max_id, l.id AS min_id, CONCAT(r.id, '<>', l.id) AS source FROM entities r, entities l WHERE r.id > l.id;"
    )
    # Remove pairs where a matching name exists:
    con.execute(
        "DELETE FROM non_pairs np "
        "USING names nma, names nmi "
        "WHERE nma.norm = nmi.norm AND np.max_id = nma.entity_id AND np.min_id = nmi.entity_id;"
    )
    # Make actual name pairs:
    con.execute("""
        INSERT INTO pairs 
        SELECT nma.name AS left_name, nma.norm AS left_norm, nma.fp AS left_fp, nma.lang AS left_lang, nma.category AS left_category, 
        nmi.name AS right_name, nmi.norm AS right_norm, nmi.fp AS right_fp, nmi.lang AS right_lang, nmi.category AS right_category, 
        false AS match, 0 AS dist_norm, 0 AS dist_fp, 0.0 AS score, np.source AS source
        FROM non_pairs np 
        JOIN names nma ON np.max_id = nma.entity_id 
        JOIN names nmi ON np.min_id = nmi.entity_id;
    """)


def compute_scores():
    log.info("Computing distances and scores...")
    con.execute("UPDATE pairs SET dist_norm = levenshtein(left_norm, right_norm);")
    con.execute("UPDATE pairs SET dist_fp = levenshtein(left_fp, right_fp);")
    con.execute("""
        UPDATE pairs SET score = GREATEST(
                (1.0 - (dist_norm::FLOAT / GREATEST(LENGTH(left_norm)::FLOAT, LENGTH(right_norm)::FLOAT))),
                (1.0 - (dist_fp::FLOAT / GREATEST(LENGTH(left_fp)::FLOAT, LENGTH(right_fp)::FLOAT)))
        );
    """)


def export_pairs():
    log.info("Exporting pairs...")
    path = Path("pairs.csv").resolve().as_posix()
    con.execute(f"COPY pairs TO '{path}';")


def init_stuff():
    logging.basicConfig(level=logging.INFO)
    con.create_function(
        "normalize_name",
        normalize_name,
        parameters=[duckdb.typing.VARCHAR, duckdb.typing.VARCHAR],
        return_type=duckdb.typing.VARCHAR,
        null_handling="special",
    )
    con.create_function(
        "fingerprint_name",
        fingerprint_name,
        parameters=[duckdb.typing.VARCHAR, duckdb.typing.VARCHAR],
        return_type=duckdb.typing.VARCHAR,
        null_handling="special",
    )
    # con.create_function(
    #     "ref_score",
    #     ref_score,
    #     parameters=[duckdb.typing.VARCHAR, duckdb.typing.VARCHAR],
    #     return_type=duckdb.typing.FLOAT,
    #     null_handling="special",
    # )


if __name__ == "__main__":
    init_stuff()
    # load_statements()
    # load_resolver()
    # make_names_table()
    # generate_name_norms()
    # compute_pairs()
    # compute_non_pairs()
    # compute_scores()
    export_pairs()

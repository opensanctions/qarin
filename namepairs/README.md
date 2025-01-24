

```sql
CREATE TABLE statements AS SELECT * FROM read_csv('/Users/pudo/Data/statements.csv', header=true);
CREATE TABLE names AS
    SELECT canonical_id AS entity_id, schema, value AS name, lang, dataset
        FROM statements
        WHERE prop_type = 'name' AND prop <> 'weakAlias' AND 
          schema IN ('Company', 'Organization', 'Person', 'PublicBody');
ALTER TABLE names ADD COLUMN category VARCHAR;
UPDATE names SET category = IF(schema = 'Person', 'PER', 'ORG');

SELECT ROWID,
           ROW_NUMBER() OVER (
               PARTITION BY name, entity_id
               ORDER BY lang DESC, ROWID
           ) AS rn
    FROM names


SELECT COUNT(*) FROM names nl, names nr
    WHERE
        nl.category = nr.category
        AND nl.norm <> nr.norm
        AND nl.entity_id > nr.entity_id;

CREATE TABLE match_pairs AS
    SELECT nl.name as left_name, nl.lang AS left_lang,
           nr.name AS right_name, nr.lang AS right_name,
           nr.entity_id FROM names nl, names nr
    WHERE nl.entity_id = nr.entity_id AND LOWER(nl.name) > LOWER(nr.name);

WITH matching_pairs AS (
    SELECT mnl.entity_id AS nle, mnr.entity_id AS nri
    FROM names mnl, names mnr
    WHERE mnl.norm = mnr.norm
        AND mnl.entity_id > mnr.entity_id
        AND mnl.norm IS NOT NULL
)
SELECT nl.name as left_name, nl.lang AS left_lang,
           nr.name AS right_name, nr.lang AS right_name,
           nr.entity_id FROM names nl, names nr
    WHERE NOT EXISTS (
            SELECT 1 FROM matching_pairs
                WHERE nl.entity_id = matching_pairs.nle AND nr.entity_id = matching_pairs.nre
        )
        AND nl.category = nr.category
        AND nl.entity_id > nr.entity_id
    LIMIT 5000;


CREATE TABLE ma_pairs AS SELECT mnl.entity_id AS nle, mnr.entity_id AS nri
    FROM names mnl, names mnr
    WHERE mnl.norm = mnr.norm
        AND mnl.entity_id > mnr.entity_id
        AND mnl.norm IS NOT NULL;

SELECT nl.name as left_name, nl.lang AS left_lang,
           nr.name AS right_name, nr.lang AS right_name,
           nr.entity_id
    FROM names nl, names nr
    WHERE NOT EXISTS (
            FROM ma_pairs
                WHERE nl.entity_id = ma_pairs.nle AND nr.entity_id = ma_pairs.nre
        )
        AND nl.category = nr.category
        AND nl.entity_id > nr.entity_id
    LIMIT 5000;

WITH matching_pairs AS (
    SELECT mnl.entity_id AS nle, mnr.entity_id AS nri
    FROM names mnl, names mnr
    WHERE mnl.norm = mnr.norm
        AND mnl.entity_id > mnr.entity_id
        AND mnl.norm IS NOT NULL
) SELECT * FROM matching_pairs;

SELECT nl.name, nl.entity_id, nr.name, nr.entity_id
    FROM names nl, names nr
    WHERE nl.norm = nr.norm
        AND nl.entity_id > nr.entity_id
        AND nl.norm IS NOT NULL;


SELECT nl.name, nl.entity_id, nr.name, nr.entity_id
    FROM resolver res
        LEFT JOIN names nl ON nl.entity_id = res.left_id
        LEFT JOIN names nr ON nr.entity_id = res.right_id
    WHERE res.judgement IN ('unsure', 'negative')
     AND nl.name > nr.name;

UPDATE resolver rx SET left_id = ry.left_id FROM resolver ry WHERE rx.left_id = ry.right_id AND ry.judgement = 'positive' AND rx.judgement <> 'positive';
UPDATE resolver rx SET right_id = ry.left_id FROM resolver ry WHERE rx.right_id = ry.right_id AND ry.judgement = 'positive' AND rx.judgement <> 'positive';


CREATE TABLE non_pairs AS SELECT GREATEST(left_id, right_id) AS max_id, LEAST(left_id, right_id) AS min_id FROM resolver WHERE judgement IN ('unsure', 'negative');

INSERT INTO non_pairs WITH entities AS (SELECT DISTINCT entity_id AS id FROM names WHERE STARTS_WITH(id, 'Q') USING SAMPLE 1000 ROWS) SELECT r.id AS max_id, l.id AS min_id FROM entities r, entities l WHERE r.id > l.id;

INSERT INTO non_pairs WITH entities AS (SELECT DISTINCT entity_id AS id FROM names WHERE STARTS_WITH(id, 'interpol') USING SAMPLE 1000 ROWS) SELECT r.id AS max_id, l.id AS min_id FROM entities r, entities l WHERE r.id > l.id;

DELETE FROM non_pairs np
    USING names nma, names nmi
    WHERE nma.norm = nmi.norm AND np.max_id = nma.entity_id AND np.min_id = nmi.entity_id;


UPDATE pairs SET score = GREATEST(
                (1.0 - (dist_norm::FLOAT / GREATEST(LENGTH(left_norm)::FLOAT, LENGTH(right_norm)::FLOAT))),
                (1.0 - (dist_fp::FLOAT / GREATEST(LENGTH(left_fp)::FLOAT, LENGTH(right_fp)::FLOAT)))
        );

SELECT (dist_norm::FLOAT / GREATEST(LENGTH(left_norm)::FLOAT, LENGTH(right_norm)::FLOAT)) FROM pairs;
```
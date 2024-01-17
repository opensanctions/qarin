# What's the problem?

* Technical variance
    * e.g. `John Smith` becomes `JOHNSMITH`
    * Spaces, extra text at the end and beginning, etc.
    * Relevant: [SWIFT message formatting](https://en.wikipedia.org/wiki/SWIFT_message_types), especially Message Types (MT) 103, 940.
* Spelling errors
    * `Alexander` becomes `Alexxander`, `Friedrich` becomes `Freidrich`
    * Often: a bored bureaucrat dealing with "foreigners"
* Transliteration and translation errors
    * `Oleksandr` becomes `Alexander`
* Cultural equivalence
    * `Alexander` becomes `Sasha`, `Robert` becomes `Bob`
* Straight-up lookup based variance
    * Western companies totally renaming as they go into China

## Name frequency

Basically: how likely is it that a person called `John Smith` is unique? This is a great question to ask in internal deduplication, but not relevant at all in sanctions screening. Do we still want to work on it?

* See [followthemoney-compare](https://github.com/alephdata/followthemoney-compare)

## Companies

* Abbreviation
    * `Gesellschaft mit beschränkter Haftung` becomes `GmbH`
* Numbering
    * `Berlin Invest II, sarl` <> `Berlin Invest III, sarl`

## Out of scope

* Multi-attribute matching (e.g. dates of birth, registration numbers), see `rigour`.
* Things we may want to circumvent if we can:
    * Parsing name strings (`John Maynard Keynes`) into named parts
    * Determining human gender based on name
    * Determining nationality (!) based on name
* Extracting names from descriptive text

## The Law

### OFAC

The US sanctions authority got into a whole discussion with the industry it regulates about how to do name matching. They seem unhappy they did that.

See: 
* [Assessing OFAC Name Matches](https://ofac.treasury.gov/faqs/topic/1591)
* [How is the Score calculated?](https://ofac.treasury.gov/faqs/249)

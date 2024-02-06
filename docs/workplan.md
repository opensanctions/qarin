# What are we going to do?

## Workstream: Testing the old 

* Send test data through nomenklatura, does it tell us interesting things?

## Workstream: Data creation 

* What failure modes of name comparison are there? doc / taxonomy
* What types of names are there?

* Tool: Name breaker (TM)
    * What does breaking a name mean in a non-alphabet language?
    * Can breaking make false positives?
* Experiment: Make a name matching dataset from Faker
    * explicitly include failure modes. Which ones can we include?
    * Is this diverse enough for our usecase?
* Experiment: Make a name matching dataset from OpenSanctions
* Experiment: Make a name matching dataset from Wikidata
* Experiment: Make a name matching dataset from JRC-Names
* How can we make false positives?
    * "Hard negatives mining" - edge cases


## Workstream: Building the new

* What is the unit of training?
    [(name, name_part), ('Friedrich Lindenberg', 'full_person'), ('Lindenberg', 'last_person')]
* How to properly evaluate? How do we make sure we don't overfit our own evaluation set?


## Workstream: Do it live!

* Are the new models/algorithms fast enough?
    * Optimize memory usage


## Workstream: What the fuck is this?

* Web site, presentation of some form?
* Make it testable online.
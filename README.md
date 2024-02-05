# Qarin: better name matching for screening tools

This repository contains the discussion materials and output for a research project into name matching in screening tools. Name matching is a difficult tasks which aims to traverse both technical and cultural variations in how a human or company name is expressed. This project will establish a framework for name matching quality assessment, build relevant open data sets, and eventually propose some open source algorithms.

## Repository Structure

The repository is structured as follows:

* `data/` contains scripts to generate and process the data sets used in the project.
* `docs/` contains the project documentation.
* `qarin/` contains the source code for the Qarin library.
    * `evaluate/` contains the code for the evaluation of name matching algorithms.
    * `match/` contains the code for the name matching algorithms.
    * `train/` contains the code for the training of name matching algorithms.
* `tests/` contains the unit tests for the Qarin Name Matching library.

## License and funding

Qarin is licensed under the terms of the MIT license, included in `LICENSE`.

Funded by the European Union. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or European Commission. Neither the European Union nor the granting authority can be held responsible for them. Funded within the framework of the [NGI Search](https://www.ngisearch.eu/) project under grant agreement No 101069364.

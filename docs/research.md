# Relevant existing work

## Industry

* Really interesting reading: https://developer.screena.ai/#introduction 
* OpenRefine normalisation documentation: https://openrefine.org/docs/technical-reference/clustering-in-depth
* [probablepeople](https://parserator.datamade.us/probablepeople/): a name component parser, open source

* International Components for Unicode: transliteration info in Unicode
    * ICU interactive tool: https://icu4c-demos.unicode.org/icu-bin/translit 
    * [PyICU](https://pypi.org/project/PyICU/)


## OCCRP

### Friedrich's early works

* `fingerprints` [code](https://github.com/alephdata/fingerprints)
    * Originally tried to emulate the OpenRefine fingerprinting algorithm
    * Now also has [company type mappings](https://github.com/alephdata/fingerprints/blob/main/fingerprints/types/types.yml)
    * Will be moved into `rigour` codebase
* `normality` [code](https://github.com/pudo/normality)
    * Utility library for doing transliteration on top of PyICU
* Project "Synonames"
    * Attemt to build synonym expansion data, i.e. Alexander -> Oleksandr, Aleksandr
    * Write-up: [An Александр by any other name](https://medium.com/occrp-unreported/an-%D0%B0%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80-by-any-other-name-819525c82d8)
    * Code: https://github.com/alephdata/synonames 

### Micha Gorelik

Consulted for OCCRP on record linkage - we should call [Micha](https://micha.codes/) and pick some brains...

* [followthemoney-predict](https://github.com/alephdata/followthemoney-predict/tree/master)
* [followthemoney-compare](https://github.com/alephdata/followthemoney-compare) contains lots of cool word on name frequencies
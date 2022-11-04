# Elementary flow mapping

## Current status

This directory has a notebook to extract the elementary flow mapping *input* files for ecoinvent version 3.6 to 3.9. Please note the following:

* There were some incorrect CAS numbers. We fixed the ones which were obviously wrong (incorrect check digits).
* The `/` separator is terrible - this character appears in many strings, including synonyms. The notebook allows for a configurable character to be used, but the default is `|`.
* The [input ecoinvent flow list](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources/blob/master/Mapping/Input/Flowlists/ecoinventEFv3.7.csv) doesn't use `/` as a separator consistently - it uses `;` to separate the field "Second CAS". We use one consistent separating character.
* The labels "CASNo" and "Second CAS" seem inconsistent, but are part of the standard.
* The [input ecoinvent flow list](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources/blob/master/Mapping/Input/Flowlists/ecoinventEFv3.7.csv) has duplicated values in the column "Second CAS", which are removed.
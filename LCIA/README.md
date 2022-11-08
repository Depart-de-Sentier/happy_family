# LCIA data format

THe proposal is to use the [LCIAformatter](https://github.com/USEPA/LCIAformatter) format, with the following changes:

* Regionalized CFs should be provided as maps, not in line with site-generic CFs. The detailed standard for the provision of regionalized CFs maps is covered in ().
* Addition of a `datapackage.json` file which provides additional metadata.
* The use of elementary flows lists other than `fedelemflowlist` is allowed; the elementary flow lists are specified as a metadata attribute.
* The use of separator characters other than `/` is allowed and recommended; the separator character, *and the columns it is applicable to*, are specified as metadata attributes.

## CSV data format

For data exchange, site-generic characterization factors **must** be provided as CSV files. Provision in other formats (spreadsheets, column-based storage formats, etc.) is explicitly not allowed in order to maximize compatibility.

### Format specification

The format is a modification of `LCIAformatter`:

 Index | Field | Type | Required |  Note |
| ---- | ------ |  ---- | ---------| -----  |
 0 | Method | string | Y | The LCIA method name, e.g. 'Traci 2.1' |
 1 | Method UUID | string | Y | ID for the method  |
 2 | Indicator | string | Y | Name of indicator, e.g. 'Acidification Potential' |
 3 | Indicator UUID| string | Y | ID for the indicator |
 4 | Indicator unit | string | Y | The unit for the indicator, e.g. 'kg CO2 eq' |
 5 | Flowable | string | Y | The flow name, e.g. 'Sulfur dioxide' |
 6 | Flow UUID | string | Y | ID of the flow |
 7 | Context | string | Y | A path-like set of context compartments in the form of directionality/environmental media/environmental compartment, e.g. 'emission/air/tropophere' |
 8 | Unit | string | Y | Unit of the flow. Uses olca-ipc.py units
 9 | CAS No | string | N | CAS number
 ~~10~~ | ~~Location~~ | 
 ~~11~~ | ~~Location UUID~~ |
 10 | Characterization factor | float | Y | LCIA characterization factor

### To be discussed

* There is no way to specify uncertainty, or to provide sampled values which would include correlated uncertainty.
* The unit column claims to use a standard specified in `olca-ipc.py`; however, this is not a standard but rather a collection, and seems not to have a design philosophy or any consistency.



# LCIA data format

The proposal is to use the [LCIAformatter](https://github.com/USEPA/LCIAformatter) format, with the following changes:

* Regionalized CFs should be provided as maps, not in line with site-generic CFs. The detailed standard for the provision of regionalized CFs maps is covered in the [Regionalized LCIA data standard](https://github.com/cmutel/regionalized-lcia-data-standard) repo.
* Addition of a `datapackage.json` file which provides additional metadata.
* The use of elementary flows lists other than `fedelemflowlist` is allowed; the elementary flow lists are specified as a metadata attribute.
* The use of separator characters other than `/` is allowed and recommended; the separator character, *and the columns it is applicable to*, are specified as metadata attributes.
* The `Indicator` field allows for multiple values, separated by the given separation character. This is needed as some indicator specifications may be up to 5 elements long.

## CSV data format

For data exchange, site-generic characterization factors **must** be provided as CSV files. Provision in other formats (spreadsheets, column-based storage formats, etc.) is explicitly not allowed in order to maximize compatibility, and because CSV data provision is a requirement for the `tabular-data-package` specification. 

### Format specification

The format is a modification of `LCIAformatter`:

 Index | Field | Type | Required |  Note |
| ---- | ------ |  ---- | ---------| -----  |
 0 | Method | string | Y | The LCIA method name, e.g. 'Traci 2.1' |
 1 | Method UUID | string | Y | ID for the method  |
 2 | Indicator | string | Y | Name of indicator, e.g. 'Acidification Potential'. Multiple values are allowed, as in `Context` |
 3 | Indicator UUID| string | Y | ID for the indicator |
 4 | Indicator unit | string | Y | The unit for the indicator, e.g. 'kg CO2 eq' |
 5 | Flowable | string | Y | The flow name, e.g. 'Sulfur dioxide' |
 6 | Flow UUID | string | Y | ID of the flow |
 7 | Context | string | Y | A path-like set of context compartments in the form of directionality/environmental media/environmental compartment, e.g. 'emission/air/tropophere' |
 8 | Unit | string | Y | Unit of the flow. Uses [`olca-ipc.py`](https://github.com/GreenDelta/olca-ipc.py/blob/master/olca/units/units.csv) units
 9 | CAS No | string | N | CAS number
 ~~10~~ | ~~Location~~ | 
 ~~11~~ | ~~Location UUID~~ |
 10 | Characterization factor | number | Y | LCIA characterization factor

### To be discussed

* There is no way to specify uncertainty, either with distributions functions or sampled values which include correlated uncertainty.
* The `Unit` column claims to use a standard specified in [`olca-ipc.py`](https://github.com/GreenDelta/olca-ipc.py/blob/master/olca/units/units.csv); however, this is not a standard but rather a collection of stuff, and seems not to have a design philosophy or any consistency.

## Metadata JSON file

The `metadata.json` file follows the [`tabular-data-package`](https://dataprotocols.org/tabular-data-package/) standard. Here is an example of the main metadata attributes:

```javascript
{
  "profile": "tabular-data-package",
  "name": string, # See spec for requirements
  "description": string,
  "id": string,
  "licenses": list,
  "resources": list,
  "created": string, # datetime encoded as string with timezone following ISO 8601
}    
```

There must be at least one resource. Here is an example of a resource metadata section:

```javascript
    {
      "path": string,
      "profile": "tabular-data-resource",
      "mediatype": "text/csv",
      "separator": string,
      "schema": {
        "fields": [
          {
            "name": "Method",
            "type": "string"
          },
          {
            "name": "Method UUID",
            "type": "string"
          },
          {
            "name": "Indicator",
            "type": "string",
            "separated": true
          },
          {
            "name": "Indicator UUID",
            "type": "string"
          },
          {
            "name": "Indicator unit",
            "type": "string"
          },
          {
            "name": "Flowable",
            "type": "string"
          },
          {
            "name": "Flow UUID",
            "type": "string"
          },
          {
            "name": "Context",
            "type": "string",
            "separated": true
          },
          {
            "name": "Unit",
            "type": "string"
          },
          {
            "name": "CAS No",
            "type": "string"
          },
          {
            "name": "Characterization factor",
            "type": "number"
          }
        ]
      }
    }
```

### More explicit string separation

The separation character is specified *per resource* in the metadata section, and the *columns which can have separated values* are indicated per column with the attribute `"separated": true`.

## Ecoinvent example data

This directory has a notebook to extract the LCIA implementation for ecoinvent version 3.9, and the output files produced.

# Elementary flow mapping

Elementary flow lists are provided following the [GLAD Flow List standard](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources/blob/master/Formats/FlowList.md), with the following changes:

* Provision of an additional metadata file
* The character used to separate strings inside a CSV field is configurable

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

This directory has a notebook to extract the elementary flow mapping *input* files for ecoinvent version 3.6 to 3.9, and the output files produced. Please note the following:

* There were some incorrect CAS numbers. We fixed the ones which were obviously wrong (incorrect check digits).
* The `/` separator is not a great choice, as it often occurs in text, and in particular in the `Synonyms`. The notebook allows for a configurable character to be used, but the default is `|`.
* The [input ecoinvent flow list](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources/blob/master/Mapping/Input/Flowlists/ecoinventEFv3.7.csv) doesn't use `/` as a separator consistently - it uses `;` to separate the field "Second CAS". We use one consistent separating character.
* The [input ecoinvent flow list](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources/blob/master/Mapping/Input/Flowlists/ecoinventEFv3.7.csv) has duplicated values in the column "Second CAS", which are removed.
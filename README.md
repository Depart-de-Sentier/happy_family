# A big `happy_family`: Exchanging and using LCA community data

We are at an inflection point where the dream of LCA data compatibility could become a reality. However, there is still some work to do to achieve this vision. The repository is one place where discussion, data, metadata, and code samples can be collated to support data exchange. It is built on, and draws from, the following similar initiatives:

* [GLAD Elementary Flow Resources](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources)
* [LCIAformatter](https://github.com/USEPA/LCIAformatter/tree/master/lciafmt)
 
## Short and unique identifiers for database releases.
 
Challenge:
 
We don't call releases the same thing, meaning that it is harder than it should be for me to share a foreground inventory which builds on another inventory
 
Proposal:
 
The ecoinvent team at the Brightcon hackathon proposed the following (https://github.com/brightway-lca/hackathons/issues/1).
 
`<database namespace>-<version>-<optional additional identifiers>`
 
Rules:
 
* Use hyphens, not underscores
* No spaces (could be discussed)
* Database namespace is controlled on a first come-first serve basis, or allocated by a committee
* Version is not sortable (1.1, 1.2, 1.10 problem)
* Additional identifiers can include more than one string separated by hyphens, and are optional
* Hyphens can be in namespace or additional identifiers, and therefore separating by hyphen is not supported
 
Obviously this is not enough information; similarly to the SPDX, we would also need a registry of metadata. I think the easiest here would be just a GitHub repo with metadata provided as JSON, and GitHub actions that run on pull requests to make sure things are formatted correctly before they can get merged.
 
Conditions for success:
 
* Buy in from other database generators or distributors (e.g. Nexus, SimaPro)
* Participation in the registry
 
## LCIA data

**See https://github.com/Depart-de-Sentier/happy_family/blob/main/LCIA/README.md for a specific proposal and working example.**
 
We have LCIA XML formats in ecospold 1 (dead and buried), SimaPro CSV, olca-schema, ILCD, [lciafmt](https://github.com/USEPA/LCIAformatter), and the UNEP-SETAC [recommendation for regionalized LCIA](https://github.com/cmutel/regionalized-lcia-data-standard).
 
Challenge:
 
The CSV-based approaches (lciafmt and UNEP) are much easier to work with; there is a reason why no LCIA method developers (to the best of our knowledge) have produced XML files. However, none of the existing formats get all the details correct.
 
`lciafmt` is the closest, but:
 
* It is only the CSV, and important metadata is missing. Many data scientists have seen this pattern before, and have developed the [datapackage](https://specs.frictionlessdata.io/data-package/) spec for solving this problem. Data which is missing but absolutely vital includes data generators, URLs, and licenses.
* It uses the `/` character for separating strings, though this can appear in elementary flow names and contexts, and therefore requires escaping (not trivial for all users). A better alternative is to specify the separation character in the metadata, and to choose a character or character group which doesn't appear in the data.
* It doesn't have a proper [implementation of regionalization](https://link.springer.com/article/10.1007/s11367-018-1539-4).
* It assumes the use of [one elementary flow mapping list](https://github.com/USEPA/Federal-LCA-Commons-Elementary-Flow-List).
  
Conditions for success:
 
* Buy in from US EPA and ecoinvent. This would be enough to push the LCIA community (IMHO).
 
## LCI updates
 
Challenge:
 
Updating inventory databases already in software from one release to the next is (to the best of my knowledge) manual, painful, and certainly inconsistent. We need a data format to express these migrations such that they can be applied automatically and in a (quasi-)software independent way.
 
Proposal:
 
We develop a CSV format based closely around the elementary flow mapping format (https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources), but again with a `datapackage.json` which gives licenses, etc. This would need to be modified for the following:
 
* Verbs: The standard CRUD verbs would apply, but I think we also need "aggregate" and "disaggregate". Are there more verbs?
* I guess we need to separate changes to exchanges from changes to activities/processes - this is the approach taken by https://github.com/brightway-lca/dardanelles. One file for activities/processes and another for exchanges OK with people?
* How to handle changes in activity properties - or, in general, any change which is 3 layers deep (i.e. key: hash table)? Ideally this nested data could be unrolled to a "tidy" form (https://cran.r-project.org/web/packages/tidyr/vignettes/tidy-data.html). TO BE DISCUSSED!
 
The intention here is not to represent all possible data in the source XMLs in a CSV form (this wouldn't work), but rather the essential information needed to continue using foreground inventories build on an older background.
 
This proposal is the least developed, but perhaps the most pressing, as ecoinvent 3.9 was released moments ago :)
 
## Elementary flow mapping
 
[We have it](https://github.com/UNEP-Economy-Division/GLAD-ElementaryFlowResources). Now what?
 
We need:
 
* A `datapackage.json` file, or similar system for such metadata, sorry to repeat myself but licenses matter...
* Examples of how to actually use these mappings in several programming languages
* A plan for how such mappings can be maintained. I guess most of us don't think the development process is a reasonable candidate for maintenance... Tomas Navarrete and I built an alternative workflow here based on templates for crowd sourcing combined with GitHub actions: https://github.com/brightway-lca/simapro_ecoinvent_elementary_flows



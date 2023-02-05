# Data-analysis for the Toronto bike-share-dataset
## Folder structure
* bike_share: includes the sources (utility-functions) to be used from
* data: .gitignore-d folder, the data downloaded (and its consolidated versions) are placed here
* entry_points: python-files containing a "main()"-function each that should be used for batch-processing.
* notebooks: ipynb-files used for the data-analysis (mainly vizualization and text -- move code to proper functions in python-files into "bike_share/*" and import it for use)
* test: place tests here -- we use pytest as framework
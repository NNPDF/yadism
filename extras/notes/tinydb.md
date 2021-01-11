# TinyDB

## Input
- 1 db w 3 (or more) tables:
  - theories
    - is a view
    - generated from other tables
  - dis_observables
  - pdf_sets
    - currently part of the theory
    - stripped from theory asap
  - scale_variations (`xiR` - `xiF`)
- function to damp query result in one or multiple `yaml`
  - iterate over query and dump with `yaml.dump`

## Output

### Cache

- 1db for apfel cache

### Logs

- 1db for our output tables

# TinyDB Viewer
https://pypi.org/project/tinydb-viewer/

you can interface with jupyter

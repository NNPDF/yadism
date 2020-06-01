# Contributing to Yadism

If you are not a member of development team pleas look below for [external
contributions guidelines](.github/contributing.md#external-contributions)

## Internal development

### Unit Tests
To run test install the package and run `pytest tests` in the project root
(configurations are in `setup.cfg`).

<!--TODO further descriptions should be moved to the wiki, in order to have a
unique place to reference for development and to keep this document as short as
possible-->

#### Markers
Show known marks with `pytest --markers` and run them with:
- quick check: `pytest -m quick_check`
- commit check: `pytest -m "quick_check or commit_check"`
- full check: `pytest`

#### Test coverage
Use `pytest ... --cov=src` to obtain a report for test coverage.

### Benchmarks and regression tests
Since there is a non-trivial framework to manage these tasks you should look
into the specific
[documentation](https://n3pdf.github.io/yadism/dev-tools/db-suite.html).

The main idea is to generate the input databases customizing and running
provided scripts, and then select with suitable queries the combinations of
input you are interested in, and running the benchmark utility passing the
queries as arguments.

### Release based workflow
Since we are adopting a release based workflow choose a *suitable base* for your
*pull request*:
- if you are submitting a quick fix, or small proposal, choose as base a
 `feature/**/*` or `release/**/*` branch
- if you are setting up a major update (i.e. your new branch itself is a
 `feature/**/*` or `release/**/*` one) choose as base `master`

## External contributions

Currently the main guideline we would like to highlight is to use [GitHub
issues](https://github.com/N3PDF/yadism/issues) for requests, bugs reporting,
and any other communication, and [GitHub pull
requests](https://github.com/N3PDF/yadism/pulls) for code contributions.

External pull requests should be applied to the latest release branch, if not
available choose simply `master` as base, and it will be moved to a suitable one
by maintainers.

Please take the time to fulfill the proper template (it will be automatically provided).


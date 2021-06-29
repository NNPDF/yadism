# Contributing to Yadism

If you are not a member of development team pleas look below for [external
contributions guidelines](.github/contributing.md#external-contributions)

## Internal development

### Release based workflow

The development it's following some conventions to improve collaboration:

- the _almost_ standard [SemVer](https://semver.org/) it's adopted for versions'
  numbers
- the popular [git flow
  model](https://nvie.com/posts/a-successful-git-branching-model/) it's used for
  managing git branches
  - in order to help you with the management consider using [`git flow`](https://github.com/petervanderdoes/gitflow-avh) CLI tool (and the corresponding [shell completion](https://github.com/petervanderdoes/git-flow-completion)), or the original version of [`git flow`](https://github.com/nvie/gitflow).

#### Caveat

- remember to base all the pull requests on GitHub to `develop` (and not
  `main`/`master`)
- while using `git flow` to merge remember to use the `-k` (keep) option, for
  GitHub compatibility

### Installation

#### Dev Dependencies

Install the other dependencies using:

```
pip install -r dev_requirements.txt --ignore-installed
pre-commit install
```

### Unit Tests

To run test install the package and run `pytest tests` in the project root
(configurations are in `setup.cfg`).

<!--TODO further descriptions should be moved to the wiki, in order to have a
unique place to reference for development and to keep this document as short as
possible-->

#### Test coverage

Use `pytest ... --cov=src` to obtain a report for test coverage.

### Benchmarks and regression tests

Currently this package has two non-python test dependencies:

- `lhapdf`, provides PDF sets, only required for benchmarks
- `apfel`, only required for benchmarks

For `apfel` and `lhapdf` you should get them following the instructions on their
respective official distribution sources.
Than make sure to make them available in your python (virtual)environment.

## External contributions

Currently the main guideline we would like to highlight is to use [GitHub
issues](https://github.com/N3PDF/yadism/issues) for requests, bugs reporting,
and any other communication, and [GitHub pull
requests](https://github.com/N3PDF/yadism/pulls) for code contributions.

External pull requests should be applied to the latest release branch, if not
available choose simply `master` as base, and it will be moved to a suitable one
by maintainers.

Please take the time to fulfill the proper template (it will be automatically provided).

# Contributing to Yadism

If you are not a member of development team pleas look below for [external
contributions guidelines](.github/contributing.md#external-contributions).

## Internal development

### Branching model

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
- while using `git flow` to merge feature branches remember to use the `-k`
  (keep) option, for GitHub compatibility (such that the PR will result merged,
  and not closed)

### Installation

#### Development tools

Please, install in your favorite way the following tools:

- `poetry`, follow [installation
  instructions](https://python-poetry.org/docs/#installation)
- `poetry-dynamic-versioning`, used to manage the version (see
  [repo](https://github.com/mtkennerly/poetry-dynamic-versioning))
- `pre-commit`, to run maintenance hooks before commits (see
  [instructions](https://pre-commit.com/#install))

### Unit Tests

To run test install the package and just run `pytest` in the project root
(configurations are in `pyproject.toml`).

## External contributions

Currently the main guideline we would like to highlight is to use [GitHub
issues](https://github.com/N3PDF/yadism/issues) for requests, bugs reporting,
and any other communication, and [GitHub pull
requests](https://github.com/N3PDF/yadism/pulls) for code contributions.

External pull requests should be applied to the latest release branch, if not
available choose simply `develop` as base, and it will be moved to a suitable
one by maintainers.

Please take the time to fulfill the provided template.

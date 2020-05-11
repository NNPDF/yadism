<p align="center">
  <a href="https://github.com/N3PDF/dis/actions?query=workflow%3A%22yadism%22"><img alt="Tests" src="https://github.com/N3PDF/dis/workflows/yadism/badge.svg"></a>
  <a href="https://codecov.io/gh/N3PDF/dis"><img src="https://codecov.io/gh/N3PDF/dis/branch/master/graph/badge.svg?token=qgCFyUQ6oG"/></a>
  <a href="https://www.codefactor.io/repository/github/n3pdf/dis/overview/benchmarks/small-updates"><img src="https://www.codefactor.io/repository/github/n3pdf/dis/badge/benchmarks/small-updates?s=dd1c326325585a549c157120b9f55c06e6ea2b22" alt="CodeFactor" /></a>
  <a href="https://n3pdf.github.io/dis/"><img alt="Docs" src="https://github.com/N3PDF/dis/workflows/docs/badge.svg"></a>
</p>

# DIS
Yet another DIS module.
<!--Future Badges
/github/workflow/status/N3PDF/dis/yadism

use the ones provided by shields.io:
- example: https://img.shields.io/github/workflow/status/N3PDF/dis/yadism

note: in order to make shields.io the repo must be public (or accessible to it in some way)

wanted:
- Workflows (github):
  - yadism-tests: /github/workflow/status/N3PDF/dis/yadism
  - docs: /github/workflow/status/N3PDF/dis/docs
- Test coverage:
  - codecov: /codecov/c/:vcsName/:user/:repo?token=abc123def456
- Python version/s:
  - pypi: /pypi/pyversions/:packageName
  - github: /github/pipenv/locked/python-version/:user/:repo
- Package version
  - pypi: /pypi/v/:packageName
  - github: /github/v/release/:user/:repo?sort=semver
- Dependency on 'eko':
  - /librariesio/github/:user/:repo
  - or anything else

optional:
- Release-date (github):
  - /github/release-date/:user/:repo
- Last-commit (github):
  - /github/last-commit/:user/:repo
- Downloads:
  - github: /github/downloads/:user/:repo/total
  - pypi: /pypi/:period/:packageName
License:
  - pypi-license: /pypi/l/:packageName
  - github-license: /github/license/:user/:repo
- Activity:
  - open-issues (github): /github/issues/:user/:repo
  - open-pull-requests (github): /github/issues-pr/:user/:repo
- Code size:
  - github: /github/languages/code-size/:user/:repo
-->

## Scope of the project
Provide all necessary tools to compute the DIS structure functions and related object. This project is linked closely to [EKO](https://github.com/N3PDF/eko).

## Installation
```
python setup.py install
```

## Documentation
The documentation style of this code follows closely the [numpy documentation guide](https://numpydoc.readthedocs.io/en/latest/format.html).

Docs available at: https://n3pdf.github.io/dis/

## Tests
To run test install the package and `pytest`.

Then run `pytest ...` in the root directory (configurations are in `setup.cfg`).

### Markers
Show known marks with `pytest --markers` and run them with:
- quick check: `pytest -m quick_check`
- commit check: `pytest -m "quick_check or commit_check"`
- full check: `pytest`

### Test coverage
Use `pytest ... --cov=src` to obtain a report for test coverage.

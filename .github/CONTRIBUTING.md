# How to Contribute

:tada: Thanks, for considering to contribute to yadism!

:pray: For the sake of simplicity we switch below to imperative
language, however, please read a "Please" in front of everything.

- :brain: Be reasonable and use common sense when contributing: we
  added some points we would like to highlight below
- :family: Follow our [Code of
  Conduct](https://github.com/NNPDF/yadism/blob/master/.github/CODE_OF_CONDUCT.md)
  and use the provided [Issue
  Templates](https://github.com/NNPDF/yadism/issues/new/choose)
- :1234: Use the _almost_ standard [SemVer](https://semver.org/) for version numbers

## Tools

- :envelope: [`poetry`](https://github.com/python-poetry/poetry) is the
  dependency manager and packaging back-end of choice for this
  project - see the official [installation
  guide](https://python-poetry.org/docs/#installation)
- :hash: [`poery-dynamic-versioning`](https://github.com/mtkennerly/poetry-dynamic-versioning),
  is used to update the package version based on VCS status (tags and
  commits); note that since the version is dumped in output object,
  this is to be used not only for releases, but whenever output is
  generated (and intended to be used)
- :parking: [`pre-commit`](https://pre-commit.com/) is used to enforce
  automation and standardize the tools for all developers; if you want
  to contribute to this project, install it and activate it

## Docs

- :books: in order to run the notebooks in the environment, you need first to install
  the environment kernel:
  ```sh
  poe docs-install-nb
  ```
  thanks to [Nikolai Janakiev](https://janakiev.com/blog/jupyter-virtual-envs/#add-virtual-environment-to-jupyter-notebook)

## Testing

- :elephant: Make sure to not break the old tests (unless there was a
  mistake)
- :hatching_chick: Write new tests for your new code - the coverage
  should be back to 100% if possible

## Style Conventions

### Python Styleguide

- :blue_book: Use [numpy documentation
  guide](https://numpydoc.readthedocs.io/en/latest/format.html)

### Git

- :octocat: Make sure the commit message is written properly ([This
  blogpost](https://chris.beams.io/posts/git-commit/) explains it
  nicely)

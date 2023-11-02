[![Tests Status](https://github.com/ditschi/pre-commit-hooks/actions/workflows/tests.yml/badge.svg)](https://github.com/ditschi/pre-commit-hooks/actions/workflows/tests.yml)
[![Coverage Status](https://github.com/ditschi/pre-commit-hooks/actions/workflows/coverage.yml/badge.svg)](https://github.com/ditschi/pre-commit-hooks/actions/workflows/coverage.yml)
[![Linting Status](https://github.com/ditschi/pre-commit-hooks/actions/workflows/linting.yml/badge.svg)](https://github.com/ditschi/pre-commit-hooks/actions/workflows/linting.yml)
[![Format-Check Status](https://github.com/ditschi/pre-commit-hooks/actions/workflows/format.yml/badge.svg)](https://github.com/ditschi/pre-commit-hooks/actions/workflows/format.yml)
[![Security Status](https://github.com/ditschi/pre-commit-hooks/actions/workflows/security.yml/badge.svg)](https://github.com/ditschi/pre-commit-hooks/actions/workflows/security.yml)

# pre-commit-hooks



Collection of pre-commit hooks

## Hooks availble

### protect-files

Protect tracked files from being changed accidentally. This might be useful for files which are tracked by git and therefore are not handled by the .gitifnore file. With this hook accidential changes of these files are prevented.

A list of glob patterns has to be be provided to define the files protected from changes. By default files will be automatically removed von staging area (this can be diabled).

The following args are available with this hook:

  - `--protected-files-globs` (required): one or more globs of protected files
    -  Note: pre-commit appends the fileanmes of staged files to the command. To seperate  the list of globs from the list of filenames add '--' at the end of the args list
  - `--no-unstange`: when provided the protected changed files are not automatically unstaged


#### usage:
```yaml
-   repo: https://github.com/ditschi/pre-commit-hooks
    rev: v0.1.0
    hooks:
    -   id: protect-files
        # Note: pre-commit appends the fileanmes of staged files to the command.
        #       To seperate the globs from the list of filenames add a '--'
        args: ['--protected-files-globs', '.devcontainer/*', 'my/dir/*', '--' ]

-   repo: https://github.com/ditschi/pre-commit-hooks
    rev: v0.1.0
    hooks:
    -   id: protect-files
        args: ['--protected-files-globs', '.vscode/*', --no-unstage]
```


## Devopment

The recommented way to start the development environment is using the DevContainer in vscode. Alternatively you can install and use  `tox` to setup the environment.

The following comands will help ypu to get started:

```bash
# ensure tox and pipenv is installed (alerady done in DevContainer)
python3 -m pip install tox pipenv

# run all default checks
tox

# only run the specifik test environments (note: check tox.ini foe all environments)
tox -e tests
tox -e lint

# start interactive session in venv with all modules installed
tox -e dev

# add and update dependencies using pipenv
pipenv --help # get an overview about pipenv
pipenv install --dev my-new-dependency
pipenv update
```

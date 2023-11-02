# pre-commit-hooks

Collection of pre-commit hooks

## Hooks availble

### protect-files

Protect tracked files from being changed accidentally. This might be useful for files which are tracked by git and therefore are not handled by the .gitifnore file. With this hook accidential changes of these files are prevented.

A list of glob patterns has to be be provided to define the files protected from changes. By default files will be automatically removed von staging area (this can be diabled).

The following args are available with this hook:

  - `--protected-files-globs` (required): one or more globs of protected files
  - `--no-unstange`: when provided the protected changed files are not automatically unstaged



#### usage:
```yaml
-   repo: https://github.com/ditschi/pre-commit-hooks
    rev: v0.1.0
    hooks:
    -   id: protect-files
        args: ['--protected-files-globs', '.devcontainer/*', 'my/dir/*' ]

-   repo: https://github.com/ditschi/pre-commit-hooks
    rev: v0.1.0
    hooks:
    -   id: protect-files
        args: ['--protected-files-globs', '.vscode/*', --no-unstange]
```

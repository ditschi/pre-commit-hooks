from __future__ import annotations

import argparse
import fnmatch
import subprocess
from typing import Sequence


def protected_files_changed(
    staged_files: list[str], protected_files_globs: list[str]
) -> list[str]:
    protected_changed = []
    for filename in staged_files:
        for pattern in protected_files_globs:
            if fnmatch.fnmatch(filename, pattern):
                print(f"'{filename}' is protected by pattern '{pattern}'.")
                protected_changed.append(filename)
    return protected_changed


def unstage_files(filepaths: list[str]) -> None:
    command = ["git", "reset", "--"]
    command.extend(filepaths)
    subprocess.run(command, check=False)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filenames",
        nargs="*",
        help="Filenames pre-commit believes are changed.",
    )
    parser.add_argument(
        "--protected-files-glob",
        nargs="*",
        help="One or more glob patterns to specify protected files.",
        default=[],
    )
    parser.add_argument(
        "--no-unstage",
        action="store_true",
        help="Enforce all files are checked, not just staged files.",
    )
    args = parser.parse_args(argv)

    if not args.filenames:
        return 0

    bad_files = protected_files_changed(args.filenames, args.protected_files_glob)

    if bad_files and not args.no_unstage:
        unstage_files(bad_files)

    return len(bad_files)


if __name__ == "__main__":
    raise SystemExit(main())

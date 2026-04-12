import os

import nox
from pathlib import Path

nox.options.sessions = ["tests", "format", "lint", "security", "code_analysis", "packaging_test"]
nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]


def _session_python_versions():
    """Python versions for Nox sessions.

    If NOX_PYTHON is set (CI matrix, devcontainer), only that version is used.
    Otherwise all supported versions — for local runs with multiple interpreters (e.g. pyenv).
    """
    single = os.environ.get("NOX_PYTHON", "").strip()
    if single:
        return [single]
    return PYTHON_VERSIONS


def _lockfile(session):
    return Path("requirements") / f"requirements-dev-py{session.python.replace('.', '')}.txt"


def _install(session):
    lockfile = _lockfile(session)
    if not lockfile.exists():
        session.error(f"Missing lockfile: {lockfile}. Run `nox -s lock` first.")
    session.install("-r", str(lockfile))
    session.install("-e", ".")


def _run(session, *args):
    session.run(*args, external=True)


@nox.session(python=_session_python_versions())
def tests(session):
    _install(session)
    _run(
        session,
        "pytest",
        "--html=./out/pytest/index.html",
        "--self-contained-html",
    )


@nox.session(python=_session_python_versions())
def coverage(session):
    _install(session)
    _run(session, "coverage", "erase")
    _run(session, "coverage", "run", "-m", "pytest", "tests")
    _run(session, "coverage", "report")
    _run(session, "coverage", "html", "-d", "./out/coverage")


@nox.session(python=_session_python_versions())
def lint(session):
    _install(session)
    _run(
        session,
        "flake8",
        "pre_commit_hook_collection",
        "tests",
        "--max-complexity",
        "10",
    )
    _run(session, "pylint", "pre_commit_hook_collection", "tests")
    _run(
        session,
        "mypy",
        "pre_commit_hook_collection",
        "tests",
        "--html-report",
        "./out/mypy",
        "--any-exprs-report",
        "./out/mypy/",
        "--linecount-report",
        "./out/mypy/",
        "--linecoverage-report",
        "./out/mypy/",
        "--lineprecision-report",
        "./out/mypy/",
    )


@nox.session(python=_session_python_versions())
def format(session):
    _install(session)
    _run(session, "black", "pre_commit_hook_collection", "tests")
    _run(session, "isort", "pre_commit_hook_collection", "tests")


@nox.session(python=_session_python_versions())
def security(session):
    _install(session)
    _run(session, "bandit", "pre_commit_hook_collection", "tests", "-r", "-ll")


@nox.session(python=_session_python_versions())
def code_analysis(session):
    _install(session)
    _run(session, "radon", "cc", "pre_commit_hook_collection", "tests", "-a")
    _run(session, "radon", "mi", "pre_commit_hook_collection", "tests")
    _run(session, "vulture", "pre_commit_hook_collection", "tests")


@nox.session(python=_session_python_versions())
def packaging_test(session):
    _install(session)
    _run(session, "pyroma", ".")
    _run(session, "python", "-m", "build")
    _run(session, "twine", "check", "dist/*")


@nox.session(python="3.10", name="dev")
def dev(session):
    _install(session)
    _run(session, "pre-commit", "install")
    session.log("Dev environment prepared. Use nox sessions or uv for further work.")


@nox.session(python=_session_python_versions())
def lock(session):
    session.install("pip-tools")
    session.run(
        "python",
        "-m",
        "piptools",
        "compile",
        "--output-file",
        "requirements/requirements.txt",
        "requirements/requirements.in",
        external=True,
    )
    session.run(
        "python",
        "-m",
        "piptools",
        "compile",
        "--extra",
        "dev",
        "--output-file",
        str(_lockfile(session)),
        "pyproject.toml",
        external=True,
    )

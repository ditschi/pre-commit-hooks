import nox
from pathlib import Path

nox.options.sessions = ["tests", "format", "lint", "security", "code_analysis", "packaging_test"]
nox.options.reuse_existing_virtualenvs = True

PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13", "3.14"]


def _lockfile(session):
    return Path("requirements") / f"requirements-dev-py{session.python.replace('.', '')}.txt"


def _install(session):
    lockfile = _lockfile(session)
    if not lockfile.exists():
        session.error(f"Missing lockfile: {lockfile}. Run `nox -s lock` first.")
    session.install("-r", str(lockfile))


def _uv_run(session, *args):
    session.run(
        "uv",
        "run",
        "--active",
        *args,
        external=True,
        env={"UV_LINK_MODE": "copy"},
    )


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    _install(session)
    _uv_run(
        session,
        "pytest",
        "--html=./out/pytest/index.html",
        "--self-contained-html",
    )


@nox.session(python=PYTHON_VERSIONS)
def coverage(session):
    _install(session)
    _uv_run(session, "coverage", "erase")
    _uv_run(session, "coverage", "run", "-m", "pytest", "tests")
    _uv_run(session, "coverage", "report")
    _uv_run(session, "coverage", "html", "-d", "./out/coverage")


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    _install(session)
    _uv_run(
        session,
        "flake8",
        "pre_commit_hook_collection",
        "tests",
        "--max-complexity",
        "10",
    )
    _uv_run(session, "pylint", "pre_commit_hook_collection", "tests")
    _uv_run(
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


@nox.session(python=PYTHON_VERSIONS)
def format(session):
    _install(session)
    _uv_run(session, "black", "pre_commit_hook_collection", "tests")
    _uv_run(session, "isort", "pre_commit_hook_collection", "tests")


@nox.session(python=PYTHON_VERSIONS)
def security(session):
    _install(session)
    _uv_run(session, "bandit", "pre_commit_hook_collection", "tests", "-r", "-ll")


@nox.session(python=PYTHON_VERSIONS)
def code_analysis(session):
    _install(session)
    _uv_run(session, "radon", "cc", "pre_commit_hook_collection", "tests", "-a")
    _uv_run(session, "radon", "mi", "pre_commit_hook_collection", "tests")
    _uv_run(session, "vulture", "pre_commit_hook_collection", "tests")


@nox.session(python=PYTHON_VERSIONS)
def packaging_test(session):
    _install(session)
    _uv_run(session, "pyroma", ".")
    _uv_run(session, "python", "-m", "build")
    _uv_run(session, "twine", "check", "dist/*")


@nox.session(python="3.10", name="dev")
def dev(session):
    _install(session)
    _uv_run(session, "pre-commit", "install")
    session.log("Dev environment prepared. Use nox sessions or uv for further work.")


@nox.session(python=PYTHON_VERSIONS)
def lock(session):
    session.install("pip-tools")
    session.run(
        "python",
        "-m",
        "piptools",
        "compile",
        "requirements.in",
        external=True,
    )
    session.run(
        "python",
        "-m",
        "piptools",
        "compile",
        "--output-file",
        str(_lockfile(session)),
        "requirements-dev.in",
        external=True,
    )

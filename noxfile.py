import nox
from nox import Session

nox.options.reuse_existing_virtualenvs = True

@nox.session
def tests(session: Session) -> None:
    session.install("-r", "requirements.txt")
    session.install("pytest")
    session.run("pytest", "-vv", "-s")


@nox.session
def format(session: Session) -> None:
    session.install(
        "-r", "requirements.txt",
        "flake8",
        "flake8-bandit",
        "flake8-black",
        "flake8-breakpoint",
        "flake8-bugbear",
        "flake8-isort",
    )
    session.run("black", "src", "tests")
    session.run("isort", "src", "tests")

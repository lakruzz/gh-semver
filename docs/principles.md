# Design Principles

This extension is deliberately created as a very simpl — short – codebase. It's desinged as a showcase in demonstration of coding principles that we adhere to when building software in general and Python in particular. In this document we will brievfly touch on each single one of them. But we have opende up the discussions on this repe and we hereby invite you to join these discussions and chip in with your oppionated view-points, questions, or even more principles.

**Join the [Design Principle Discussions](https://github.com/lakruzz/gh-semver/discussions) in this repo**

# GitHub CLI extensions over GitHub Actions
We should become confident with effortlessly creating gh CLI extensions to implement and support the team's common way of working. I argue that these GitHic CLI extensions are more useful - and recommendede over - GitHub actions. Actions can only run in GitHub workflows, whihc means that whatever _business logic_ is implemneted in a GitHub Action used as a quality gate is hard(er) to provide to the devloper, while in the development environement.

# When desingning CLIs - start with the interface
Well, the I in CLI[^cli] stand exactly for _interface_ so the recommendation to start with the interface may seem implicitly obvious. But the recommendation is to quire literally start with designing what the `argparser` should do and to verify that the interface is validated, before any core logic is added.

[^cli]: CLI = Command Line Interface

In this project the interface is designed in the [`parser()`](../gh_semver.py#L29) function and it's unittested individually using patches and mocks in the unit tests to that it's only the behaviour of the argparser that is verified.

# The development environment should be self contained and automated
The vision is clear. It should be possible for a (new) contributor to be able to:

1: Open the project in the IDE (VS Code)
2: Run the unittests

This should be enabled with a minimum set of requirements - we dare anyone to limit this set of requirements to:

- A *nix-like OS (MacOS, WSL, Docker, Linux...)
- The ability ro run docker on the host machine (≈Docker Desktop)
- The ability to run git commands.

Alternatively the dev environment should be able to run simply by starting a GitHub Codespace - and then run the unittests.

In this project et requires (quite a) handful of configuration files. But togeter then enable this vision:

- [`.devcontainer`](../.devcontainer/) - Defined sthe devcontainer in full. In this project there's a `devcontainer.json` and a `postCreateCommand.sh` but it could easily have contained a `Dockerfile` as well.
- [`.vscode/settings.json`](../.vscode/settings.json) - Mostly python unittest specif settings.
- [`.coveragerc`](../.coveragerc) - Defines the scope of the code coverage
- [`pytest.ini`](../pytest.ini) - Defines the scope and settings for `pytest`
- [`Pipfile.lock`](../Pipfile.lock) and [`Pipfile`](../Pipfile) - Defines the virtural python environment, controlled by `pipenv`
- [`.gitignore`](../.gitignore) and [`.gitconfig`](../.gitconfig) - Defines the git settings. `.gitignore` is required and `.gitconfig` is mostly for conveniency.

# Unittests should only depend on _the unit_
Being your developer PC (or in our case the devcontainer). It means that all unittests must run without access to a _external dependencies_ which in some instaces even include subprocess calls to the OS. To achieve this you must utilize `patches` and `mocks` in your unittests.

The test [`test_config_invalid_prefix()`](../tests/test_gh-semver-unittest.py#L82-L90) is an example on how the `stderr` from a nested call to `subprocess.run()` is designed to have a specic content to serve the test. So the code is executed witout alterizations, but the unittest itself manipulates the surroundings.

The test [`test_semver_outside_git()`](../tests/test_gh-semver-unittest.py#L193-L204) is decorating the functions with a `patch` of one of our own functions `semver.__run_git()` and then the patch is `mocked`to manitulate the return value of `__run_git()`. Same principle as above, but this time taking control of the outpur of one of our own classes.

It mays seem complex and convoluted, with abstractions on top of abstractions but rest assured that this is something that most GPTs are really good at.

# Unittests should control the test environment

The unittest class `unittest.TestCase` has at least two _keyword_ class functions that you should know of: `setup_class()` and `teardown_class()` (see [examples](https://github.com/lakruzz/gh-semver/blob/a8c079b7a67db25fc58a48e841d961d7af758064/tests/test_gh-semver-smoketest.py#L10-L24)), The `setup_class()` function is called every time the unittest class is called and `teardown_class()` is called when the class is out of scope again. Use `unittest.TestCase` class to control the contitions of your _test suites_ (one class is one suite, another class is another suite).











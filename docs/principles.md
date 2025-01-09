# Design Principles

This extension is deliberately created as a very simpl — short – codebase. It's desinged as a showcase in demonstration of coding principles that we adhere to when building software in general and Python in particular. In this document we will brievfly touch on each single one of them. But we have opende up the discussions on this repe and we hereby invite you to join these discussions and chip in with your oppionated view-points, questions, or even more principles.

**Join the [Design Principle Discussions](https://github.com/lakruzz/gh-semver/discussions) in this repo**

# GitHub CLI extensions over GitHub Actions
We should become confident with effortlessly creating gh CLI extensions to implement and support the team's common way of working. I argue that these GitHic CLI extensions are more useful - and recommendede over - GitHub actions. Actions can only run in GitHub workflows, whihc means that whatever _business logic_ is implemneted in a GitHub Action used as a quality gate is hard(er) to provide to the devloper, while in the development environement.

# When desingning CLIs - start with the interface
Well, the I in CLI[^cli] stand exactly for _interface_ so the recommendation to start with the interface may seem implicitly obvious. But the recommendation is to quire literally start with designing what the `argparser` should do and to verify that the interface is validated, before any core logic is added.

[^cli]: CLI = Command Line Interface

In this project the interface is designed in the [`parser()`](https://github.com/lakruzz/gh-semver/blob/43bc11c42b104239e8d99376951855112255c6dd/gh_semver.py#L29)

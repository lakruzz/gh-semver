# Contributing

Run your dev environment from the devcontainer, simply start it up in VS Code and run the container locally in Docker or run it in a GitHub codespace.

The `postCreateCommand` will intilize the pipenv to use by running

```
pipenv sync
```

After that, you should do ONE THING manually:

In the Command Palette in VC Code search for and select `Python: Select interpreter...`

It's likely that you are presented with several options. You should pick the one that specifically mentions `(gh-semver*)` in the title.

Now you are good to go - start by going to the testing console and let see that the test discovery runs without any issues. After that you should see two test suites:
- `test_gh-semver-smoketest.py`
- `test_gh-semver-unittests.py`

You should mainly pay attention to the the unittests. Run them, and run them again with coverage.
If you make changes to this project you should at least gurantee that coverage is the same or higher when you push to main.

The shell script `gh-semver` is not included in the tests, but you can run it from the terminal like this:

```
./gh-semver
```

You can also execute the extension as a locally installed gh extension

To install the extenison locally it's required that you gh is set up right

```shell
gh auth status # should say that you are successfull y logged in if not run...
gh auth login -p https -h github.com --web # run gh authl login -h to learn more details
```

When you are authenticated correctly install is like this:

```shell
gh extension install . 
gh semver # after the install you can use gh to invoke it. use 'gh extension remove gh-semver' to remvoe it
```

Note that end-users will install it using the global syntax:

```shell
gh extension install lakruzz/gh-semver # it will pull latest version from GitHub
gh extension upgrade gh-semver # 'upgrade' is not supported on extenions installed with the locla syntax
```

## My extension my rules!

1. No commit should be created on `main`, unless it references a GitHub issue in the commit message
2. Development branches must be clearly marked which issue they refer to
3. Develompent branches with more than one commit not reachable from `main` must be _squashed_ in to main
4. Development branches must be _fast-forward only_ when merged into `main` achive this bt _always_ rebasing your dev branch before you attempt to deliver it







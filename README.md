# gh-semver

**This utility is desinged as a GitHub Command Line extension.**

Prerequsites:
- `python3`
- `git`
- `gh`
- `*nix` _like_ OS (MacOS, Linux, WSL, Docker...)

### GitHub CLI

Browse [cli.github.com](https://cli.github.com/) to learn all about it - including hot to install it.

If you are using a devcontainer. the only thin you need to do is to make sure that it's listed as a feature in the `.devcontainer/devconainer.json` file:

```json
...
	"features": {
		...
		"ghcr.io/devcontainers/features/github-cli:1": {},
		...
	},
...
```

It's also required that you are authenticated correctly with your GitHub account.

Run:

```shell
gh auth status # should say that you are successfull y logged in if not run...
gh auth login -p https -h github.com --web # run gh authl login -h to learn more details
```
When `gh auth status` says you're cool, you install and run this `gh-semver` extension like this:

```shell
gh extension install lakruzz/gh-semver
gh semver # will show the current highest semver tag - 0.0.0 if there aren't any
gh semver -h # will reveal the syntax, each sub command `bump` and `config` also accepts a `-h` switch
gh semver bump -h
gh semver config -h
```
## Syntax

```
usage: gh_semver.py [-h] [-v] {bump,config} ...

positional arguments:
  {bump,config}
    bump         Bump the version
    config       Creates or updates the .semver.config file

options:
  -h, --help     show this help message and exit
  -v, --verbose  Enable verbose output

usage: gh_semver.py bump [-h] (--major | --minor | --patch) [--message MESSAGE] [--suffix SUFFIX] [--run | --no-run]

options:
  -h, --help            show this help message and exit
  --major               Bump the major version
  --minor               Bump the minor version
  --patch               Bump the patch version
  --message MESSAGE, -m MESSAGE
                        Additional message to add to the tag
  --suffix SUFFIX       Suffix to add to the version. Allowed characters are lowercase letters, numbers, dashes, and underscores
  --run                 Run the bump (default)
  --no-run              Do not run the bump

usage: gh_semver.py config [-h] [-v] [--prefix PREFIX] [--suffix SUFFIX] [--initial INITIAL]

options:
  -h, --help         show this help message and exit
  -v, --verbose      Enable verbose output

Configuration options:
  --prefix PREFIX    Prefix for the tag. Allowed characters are lowercase and uppercase letters
  --suffix SUFFIX    Suffix for the tag. Allowed characters are lowercase letters, numbers, dashes and underscores
  --initial INITIAL  Initial offset for the first tag. Must be a three-level integer separated by dots (e.g., 1.0.0)

```

## Note
It's written in Python and runs in a `pipenv` so it doesn't leave any footprint or alterization to your own, current Python setup. All requirements besides `python3` are managed independenly by the script itself.
# gh-semver

**This utility is desinged as a GitHub Command Line extension.**

It helps creating annotated tags in git that adhere to the rules of Semantic Versioning

The simple use case is to make sure that tags are create consistenly in the repo. And in a way where you don't have to look you the most recent semver tag in in your repo first:

### Get the current (highest) SemVer tag in the repo

```shell
gh semver
```

A SemVer tag is defined as any tag that includes a three level integer (RegExp. `\d+\.\d+\.\d+`).

It can have both a _preffix_ or a _suffix_ and still qualify. All the following examples would qualify:

- v0.0.1
- version1.1.1
- ver1.2.1
- version2.1.1-freetext
- 2.2.234

But this one wouldn't 

- version3.11-freetext

### Bump to the next - whatever that means

You can use it like this

```shell
gh semver bump --major
gh semver bump --minor
gh semver bump --patch
```
### Predifine your _prefix_ and _suffix_ for the entire repo

You might want to use a simple naming convention wher you wanb consistency like this

- v0.0.1-alpha
- v1.1.1-alpha
- v1.2.1-alpha
- v2.1.1-alpha
- v2.2.234-alpha

You can achive this by configuring _prefix_ and _suffix_ like this

```shell
gh config --prefix v --suffix alpha
```

### Get the git tag command, but don't run it

You can also just use `gh semver` to generate the `git tag ...` commands, have them printed to `stdout` for you to read, verify and manipulate before your use it

```shell
gh semver bump --major --no-run
gh semver bump --minor --no-run
gh semver bump --patch --no-run
```

So soncequntly these two commands does exaclty the same:

```shell
gh semver bump --minor
```

```shell
eval $(gh semver bump --minor --no-run)
```

More details on syntax below

_Click the headings below to expand the details on the topic_

<details><summary><h2>SemVer Basics</h2></summary>
	
>Semantic Versioning (SemVer) is's essentially a naming convention, a protocol, in which you define version numbers in three levels of integers separated by dots:
>
>`<major>.<minor>.<patch>`
>
>Then you play by the SemVer rules which goes as follows: When you make a new release, you bump one of the three levels. The semantical meaning of the three levels are as follows:
>
> **Major** is bumped if your release has features that breaks backward compatibility (e.g. a function that used to return a string now returns an integer).<br/>
> **Minor** is bumped to indicates that your release contains new features, but that they are backward compatible (e.g. the original function that returned a string is untouched, instead a new one is added, which returns an integer).<br/>
> **Patch** is bumped to indicates that no new features were added, only bugfixes or enhancements to existing ones (consequntly the _feature-level_ defined as `<major>.<minor>` is the same, but this pathc fixes something that was broken).
>
>The bump rules in semantic versioning is that if you bump a level, then all other lower levels are reset to zero using 1.2.3 as an example:
>
>Bumping major in 1.2.3 becomes 2.**0.0**<br/>
>Bumping minor in 1.2.3 becomes 1.3.**0**<br/>
>Bumping patch in 1.2.3 becomes 1.2.4
>
>SemVer's obvious use case is in versioning interfaces or individual component releases, where the protocol lays the foundation of programatically determining wether or not it's safe to update a given component or not. SemVer is the most important tool in the toolbox, when striving to kill the a bloated monolith system compound into multiple nimble individual component releases. Package mangers like `npm`, `NuGet`, `gem`etc.  always rely on SemVer.
>
> If you want a practical example - just study the [`Pipfile.lock`](./Pipfile.lock) in this repo.

</details>
<details><summary><h2>Install</h2></summary>
	
Prerequsites:
- `python3`
- `git`
- `gh`
- `*nix`_-like_ OS (MacOS, Linux, WSL, Docker...)

### GitHub CLI

Browse [cli.github.com](https://cli.github.com/) to learn all about it - including how to install `gh`.

If you are using a devcontainer. the only thin you need to do is to make sure that it's listed as a feature in the `.devcontainer/devconainer.json` file:

```json
	"features": {
		"ghcr.io/devcontainers/features/github-cli:1": {}
	}
```

It's also required that you are authenticated correctly with your GitHub account.

```shell
gh auth status # should say that you are successfull y logged in if not run...
gh auth login -p https -h github.com --web # run gh auth login -h to learn more details
```
When `gh auth status` says you're cool

![image](https://github.com/user-attachments/assets/5f417720-d7f6-4033-8d17-7628aa38a56f)

...you are ready to install and run this `gh-semver` extension like this:

```shell
gh extension install lakruzz/gh-semver
```

And if you want to upgrade

```shell
gh extension upgrade lakruzz/gh-semver
```
</details>

<details><summary><h2>Syntax</h2></summary>

Use the `-h` switch to lean the syntax 

```
gh semver             # will show the current highest semver tag - 0.0.0 if there aren't any
gh semver -h          # will reveal the syntax, each sub command `bump` and `config` also accepts a `-h` switch
gh semver bump -h
gh semver config -h
```


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
</details>

## Note
It's written in Python and runs in a `pipenv` so it doesn't leave any footprint or alterization to your own, current Python setup. All requirements besides `python3` are managed independenly by the script itself.

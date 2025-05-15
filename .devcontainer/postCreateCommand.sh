#!/usr/bin/env bash


#!/usr/bin/env bash

set -e

PREFIX="🍰  "
echo "$PREFIX Running $(basename $0)"

echo "$PREFIX Setting up safe git repository to prevent dubious ownership errors"
git config --global --add safe.directory /workspace

echo "$PREFIX Setting up git configuration to support .gitconfig in repo-root"
git config --local --get include.path | grep -e ../.gitconfig >/dev/null 2>&1 || git config --local --add include.path ../.gitconfig

echo "$PREFIX Checking if the uv environment - if needed"
if [ -e ./pyproject.toml ]; then
    echo "$PREFIX Installing uv"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "$PREFIX Creating and activating the venv"
    uv venv
    . .venv/bin/activate
    echo "$PREFIX uv syncing the dev environment"
    uv sync --extra dev
else
    echo "$PREFIX Skipping uv environment setup (no pyproject.toml found)"
fi

echo "$PREFIX Checking if the Pipenv sync - if needed"
if [ -e ./Pipfile.lock ]; then
    echo "$PREFIX Synchronizing pipenv"
    pipenv sync --dev
else
    echo "$PREFIX Skipping pipenv sync (no Pipfile.lock found)"
fi


# Check if the GH CLI is required
if [ -e $(dirname $0)/_temp.token ]; then
    echo "$PREFIX Setting up GitHub CLI"
    $(dirname $0)/gh-login.sh postcreate
    echo "$PREFIX Installing the techcollective/gh-tt gh cli extension"
    gh extension install thetechcollective/gh-tt
    echo "$PREFIX Installing the lakruzz/gh-semver gh cli extension"
    gh extension install lakruzz/gh-semver
    echo "$PREFIX Installing the gh aliases"    
    gh alias import .gh_alias.yml --clobber

fi


echo "$PREFIX SUCCESS"
exit 0




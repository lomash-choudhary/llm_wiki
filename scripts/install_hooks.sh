#!/bin/sh
set -eu

git config core.hooksPath .githooks
echo "Git hooks installed from .githooks"

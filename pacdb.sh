#!/bin/sh

export PYTHONPATH="$(cd "$(dirname "$0")" && pwd):$PYTHONPATH"

exec python3 -u -m pacdb "$@"
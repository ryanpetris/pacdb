#!/usr/bin/env python3

import os

from ..dbreader import DbReader
from ..sqldb import SqlWriter

PACMAN_SYNC_DIR = "/var/lib/pacman/sync"
PACDB_DIR = "/var/lib/pacdb"
PACDB_FILENAME = "pacman.sqlite"


def process_db(dbname: str, dbpath: str, writer: SqlWriter):
    with DbReader(dbpath) as reader:
        for pkg in reader:
            writer.write_package(dbname, pkg)


def main():
    if os.geteuid() == 0:
        if not os.path.exists(PACDB_DIR):
            os.makedirs(PACDB_DIR)

        if os.path.exists(f"{PACDB_DIR}/{PACDB_FILENAME}"):
            os.remove(f"{PACDB_DIR}/{PACDB_FILENAME}")

        database_path = f"{PACDB_DIR}/{PACDB_FILENAME}"
    else:
        if os.path.exists(PACDB_FILENAME):
            os.remove(PACDB_FILENAME)

        database_path = PACDB_FILENAME

    databases = []

    for item in os.listdir(PACMAN_SYNC_DIR):
        fullpath = f"{PACMAN_SYNC_DIR}/{item}"

        if not os.path.isfile(fullpath):
            continue

        if not item.endswith(".db"):
            continue

        databases.append({
            "name": item[:len(item) - 3],
            "path": fullpath
        })

    with SqlWriter(database_path) as writer:
        for db in databases:
            process_db(db.get('name'), db.get('path'), writer)

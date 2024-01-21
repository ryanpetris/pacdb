#!/usr/bin/env python3

import os
import shutil

from ..dbreader import DbReader
from ..sqldb import SqlWriter
from typing import Optional

PACMAN_SYNC_DIR = "/var/lib/pacman/sync"
PACDB_DIR = "/var/lib/pacdb"
PACDB_FILENAME = "pacman.sqlite"


def process_db(dbname: str, dbpath: str, filesdbpath: Optional[str], writer: SqlWriter):
    with DbReader(dbpath, filesdbpath) as reader:
        for pkg in reader:
            writer.write_package(dbname, pkg)


def main():
    if os.geteuid() == 0:
        if not os.path.exists(PACDB_DIR):
            os.makedirs(PACDB_DIR)

        database_path = f"{PACDB_DIR}/{PACDB_FILENAME}"
        database_temp_path = f"{PACDB_DIR}/.{PACDB_FILENAME}.pacdb-new"
    else:
        database_path = PACDB_FILENAME
        database_temp_path = f".{PACDB_FILENAME}.pacdb-new"

    if os.path.exists(database_temp_path):
        os.remove(database_temp_path)

    databases = []

    for item in os.listdir(PACMAN_SYNC_DIR):
        fullpath = f"{PACMAN_SYNC_DIR}/{item}"

        if not os.path.isfile(fullpath):
            continue

        if not item.endswith(".db"):
            continue

        db_name = item[:len(item) - 3]
        files_db_fullpath = f"{PACMAN_SYNC_DIR}/{db_name}.files"

        entry = {
            "name": db_name,
            "path": fullpath
        }

        if os.path.isfile(files_db_fullpath):
            entry["files_path"] = files_db_fullpath

        databases.append(entry)

    with SqlWriter(database_temp_path) as writer:
        for db in databases:
            process_db(db.get('name'), db.get('path'), db.get('files_path', None), writer)

    shutil.move(database_temp_path, database_path)

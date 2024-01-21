#!/usr/bin/env python3
import os.path
import sys

from collections.abc import Iterator
from gzip import GzipFile
from io import BytesIO
from tarfile import TarFile, TarInfo
from typing import Dict, IO, Optional, Union


class DbReader(Iterator):
    @property
    def db(self) -> str:
        return self._db

    @property
    def files_db(self) -> Optional[str]:
        return self._files_db

    def __init__(self, db: str, files_db: Optional[str] = None):
        self._db: str = db
        self._files_db: Optional[str] = files_db

    def __enter__(self):
        self._db_tar: TarFile = TarFile.open(self._db, 'r:gz')
        self._files_db_tar: Optional[TarFile] = None
        self._files_db_files: Optional[Dict[str, TarInfo]] = None

        if self._files_db:
            self._files_db_tar: TarFile = TarFile.open(self._files_db, 'r:gz')
            self._files_db_files: Dict[str, TarInfo] = self.get_files_db_files()

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._db_tar is not None:
            self._db_tar.close()
            self._db_tar = None

        if self._files_db_tar is not None:
            self._files_db_tar.close()
            self._files_db_tar = None

        if self._files_db_files is not None:
            self._files_db_files = None

        return False

    def get_files_db_files(self) -> Dict[str, TarInfo]:
        return {
            member.name: member
            for member in self._files_db_tar.getmembers()
            if member.isfile() and os.path.basename(member.name) == "files"
        }

    def get_next_file(self) -> Optional[TarInfo]:
        while True:
            item = self._db_tar.next()

            if item is None:
                return None

            if not item.isfile():
                continue

            return item

    def convert_file(self, item: TarInfo) -> Dict[str, str]:
        result = {}

        def process_lines(stream: IO[bytes]):
            nonlocal result
            field_name = None

            while True:
                line = stream.readline()

                if line == b'':
                    break

                line = line.strip(b'\n')

                if line == '':
                    continue

                if line.startswith(b'%'):
                    field_name = line.strip(b'%').decode('utf-8')
                    continue

                if not field_name:
                    break

                if field_name not in result:
                    result[field_name] = BytesIO()

                result[field_name].write(line)
                result[field_name].write(b'\n')

        with self._db_tar.extractfile(item) as f:
            process_lines(f)

        if self._files_db_tar:
            pkgname = result.get('NAME').getvalue().decode('utf-8').rstrip('\n')
            pkgversion = result.get('VERSION').getvalue().decode('utf-8').rstrip('\n')
            files_tar_info = self._files_db_files.get(f"{pkgname}-{pkgversion}/files", None)

            if files_tar_info:
                with self._files_db_tar.extractfile(files_tar_info) as f:
                    process_lines(f)
            else:
                print(f"Package {pkgname} with version {pkgversion} missing in files db. Please ensure Sync and Files databases are in sync.", file=sys.stderr)

        return {k: v.getvalue().decode('utf-8').rstrip('\n') for k, v in result.items()}

    def __next__(self) -> Dict[str, str]:
        if self._db_tar is None:
            raise StopIteration

        item = self.get_next_file()

        if item is None:
            raise StopIteration

        return self.convert_file(item)

#!/usr/bin/env python3

from collections.abc import Iterator
from gzip import GzipFile
from tarfile import TarFile, TarInfo
from typing import Dict, IO, Optional, Union


class DbReader(Iterator):
    @property
    def file(self) -> Union[str, IO[bytes]]:
        return self._file

    def __init__(self, file: Union[str, IO[bytes]]):
        self._file: Union[str, IO[bytes]] = file

    def __enter__(self):
        self._gzipfile: GzipFile = GzipFile(self._file)
        self._tarfile: TarFile = TarFile.open(fileobj=self._gzipfile)

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._tarfile is not None:
            self._tarfile.close()
            self._tarfile = None

        if self._gzipfile is not None:
            self._gzipfile.close()
            self._gzipfile = None

        return False

    def get_next_file(self) -> Optional[TarInfo]:
        while True:
            item = self._tarfile.next()

            if item is None:
                return None

            if not item.isfile():
                continue

            return item

    def convert_file(self, item: TarInfo) -> Dict[str, str]:
        result = {}
        fieldname = None

        with self._tarfile.extractfile(item) as f:
            while True:
                line = f.readline().decode('utf-8')

                if line == '':
                    break

                line = line.strip('\n')

                if line == '':
                    continue

                if line.startswith('%'):
                    fieldname = line.strip('%')
                    continue

                if fieldname not in result:
                    result[fieldname] = line
                else:
                    result[fieldname] += f'\n{line}'

        return result

    def __next__(self) -> Dict[str, str]:
        if self._tarfile is None:
            raise StopIteration

        item = self.get_next_file()

        if item is None:
            raise StopIteration

        return self.convert_file(item)

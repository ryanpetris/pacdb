#!/usr/bin/env python3

import re
import sqlite3

from .initdb import init_db_data
from .statements import insert_package_stmt, insert_package_sum_stmt, insert_package_license_stmt, insert_depends_stmt, insert_make_depends_stmt, insert_check_depends_stmt, insert_opt_depends_stmt, insert_provides_stmt, insert_conflicts_stmt, insert_replaces_stmt
from typing import Dict

class SqlWriter:
    @property
    def file(self) -> str:
        return self._file

    def __init__(self, file: str):
        self._file: str = file

    def __enter__(self):
        self._db: sqlite3.Connection = sqlite3.connect(self._file)
        self._db.executescript(init_db_data)

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._db is not None:
            self._db.commit()
            self._db.close()
            self._db = None

        return False

    def write_package(self, dbname: str, package: Dict[str, str]):
        self._write_package(dbname, package)
        self._write_package_sums(dbname, package)
        self._write_package_license(dbname, package)

        depends_types = [
            "depends",
            "make_depends",
            "check_depends",
            "opt_depends",
            "conflicts",
            "provides",
            "replaces"
        ]

        for depend_type in depends_types:
            self._write_depends(dbname, depend_type, package)

    def _write_package(self, dbname: str, package: Dict[str, str]):
        self._db.execute(insert_package_stmt, {
            "db": dbname,
            "package": package.get('NAME'),
            "base": package.get('BASE'),
            "version": package.get('VERSION'),
            "architecture": package.get('ARCH', None),
            "description": package.get('DESC', None),
            "url": package.get('URL', None),
            "download_bytes": int(package.get('CSIZE', 0)),
            "installed_bytes": int(package.get('ISIZE', 0)),
            "pgp_signature": package.get('PGPSIG', None),
            "build_timestamp": int(package.get('', 0)),
            "packager": package.get('PACKAGER', None),
            "filename": package.get('FILENAME', None)
        })

    def _write_package_sums(self, dbname: str, package: Dict[str, str]):
        sums = []

        for key, value in package.items():
            if not key.endswith('SUM'):
                continue

            sums.append({
                "db": dbname,
                "package": package.get('NAME'),
                "type": key[:len(key) - 3].lower(),
                "sum": value
            })

        if not sums:
            return

        self._db.executemany(insert_package_sum_stmt, sums)

    def _write_package_license(self, dbname: str, package: Dict[str, str]):
        licenses = package.get("LICENSE", None)

        if not licenses:
            return

        self._db.executemany(insert_package_license_stmt, [
            {
                "db": dbname,
                "package": package.get('NAME'),
                "license": l
            } for l in licenses.splitlines(keepends=False)
        ])

    def _write_depends(self, dbname: str, type: str, package: Dict[str, str]):
        if type == "depends":
            stmt = insert_depends_stmt
            packages = package.get('DEPENDS', None)
            other_package_field = "depend_package"
            has_description = False
        elif type == "make_depends":
            stmt = insert_make_depends_stmt
            packages = package.get('MAKEDEPENDS', None)
            other_package_field = "depend_package"
            has_description = False
        elif type == "check_depends":
            stmt = insert_check_depends_stmt
            packages = package.get('CHECKDEPENDS', None)
            other_package_field = "depend_package"
            has_description = False
        elif type == "opt_depends":
            stmt = insert_opt_depends_stmt
            packages = package.get('OPTDEPENDS', None)
            other_package_field = "depend_package"
            has_description = True
        elif type == "conflicts":
            stmt = insert_conflicts_stmt
            packages = package.get('CONFLICTS', None)
            other_package_field = "conflict_package"
            has_description = False
        elif type == "provides":
            stmt = insert_provides_stmt
            packages = package.get('PROVIDES', None)
            other_package_field = "provide_package"
            has_description = False
        elif type == "replaces":
            stmt = insert_replaces_stmt
            packages = package.get('REPLACES', None)
            other_package_field = "replace_package"
            has_description = False
        else:
            raise Exception("Invalid type")

        if not packages:
            return

        data = []

        for pkgname in packages.splitlines(keepends=False):
            details = self._parse_package(pkgname)

            pkgdata = {
                "db": dbname,
                "package": package.get('NAME'),
                other_package_field: details.get('name'),
                "version": details.get('version'),
                "comparator": details.get('comparator')
            }

            if has_description:
                pkgdata["description"] = details.get('description')

            data.append(pkgdata)

        self._db.executemany(stmt, data)

    def _parse_package(self, package) -> Dict[str, str]:
        match = re.match('^(?P<name>[a-z0-9@_+][a-z0-9@._+-]*)((?P<comparator>[<>=]+)(?P<version>[^:/ ]+)?)?(: *(?P<description>.*))?$', package, re.RegexFlag.IGNORECASE)

        if not match:
            raise Exception(f"Invalid package name {package}")

        return {
            "name": match.group("name"),
            "comparator": match.group("comparator"),
            "version": match.group("version"),
            "description": match.group("description")
        }

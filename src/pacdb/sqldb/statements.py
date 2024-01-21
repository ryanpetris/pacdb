#!/usr/bin/env python3

insert_package_stmt = """
    INSERT INTO packages
        (db, package, base, version, architecture, description, url, download_bytes, installed_bytes, pgp_signature, build_timestamp, packager, filename)
    VALUES
        (:db, :package, :base, :version, :architecture, :description, :url, :download_bytes, :installed_bytes, :pgp_signature, :build_timestamp, :packager, :filename);
"""

insert_sums_stmt = """
    INSERT INTO sums
        (db, package, type, sum)
    VALUES
        (:db, :package, :type, :sum);
"""

insert_licenses_stmt = """
    INSERT INTO licenses
        (db, package, license)
    VALUES
        (:db, :package, :license);
"""

insert_groups_stmt = """
    INSERT INTO groups
        (db, package, group_name)
    VALUES
        (:db, :package, :group_name);
"""

insert_depends_stmt = """
    INSERT INTO depends
        (db, package, depend_package, version, comparator)
    VALUES
        (:db, :package, :depend_package, :version, :comparator);
"""

insert_make_depends_stmt = """
    INSERT INTO make_depends
        (db, package, depend_package, version, comparator)
    VALUES
        (:db, :package, :depend_package, :version, :comparator);
"""

insert_check_depends_stmt = """
    INSERT INTO check_depends
        (db, package, depend_package, version, comparator)
    VALUES
        (:db, :package, :depend_package, :version, :comparator);
"""

insert_opt_depends_stmt = """
    INSERT INTO opt_depends
        (db, package, depend_package, version, comparator, description)
    VALUES
        (:db, :package, :depend_package, :version, :comparator, :description);
"""

insert_conflicts_stmt = """
    INSERT INTO conflicts
        (db, package, conflict_package, version, comparator)
    VALUES
        (:db, :package, :conflict_package, :version, :comparator);
"""

insert_provides_stmt = """
    INSERT INTO provides
        (db, package, provide_package, version, comparator)
    VALUES
        (:db, :package, :provide_package, :version, :comparator);
"""

insert_replaces_stmt = """
    INSERT INTO replaces
        (db, package, replace_package, version, comparator)
    VALUES
        (:db, :package, :replace_package, :version, :comparator);
"""

insert_files_stmt = """
    INSERT INTO files
        (db, package, file)
    VALUES
        (:db, :package, :file);
"""

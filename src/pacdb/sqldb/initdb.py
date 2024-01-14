#!/usr/bin/env python3

init_db_data = """
    CREATE TABLE packages (
        db TEXT,
        package TEXT,
        base TEXT,
        version TEXT,
        architecture TEXT,
        description TEXT,
        url TEXT,
        download_bytes INT,
        installed_bytes INT,
        pgp_signature TEXT,
        build_timestamp INT,
        packager TEXT,
        filename TEXT,
        PRIMARY KEY (db, package)
    );

    CREATE TABLE sums (
        db TEXT,
        package TEXT,
        type TEXT,
        sum TEXT
    );

    CREATE TABLE licenses (
        db TEXT,
        package TEXT,
        license TEXT
    );
    
    CREATE TABLE groups (
        db TEXT,
        package TEXT,
        group_name TEXT
    );

    CREATE TABLE depends (
        db TEXT,
        package TEXT,
        depend_package TEXT,
        version TEXT,
        comparator TEXT
    );
    
    CREATE TABLE make_depends (
        db TEXT,
        package TEXT,
        depend_package TEXT,
        version TEXT,
        comparator TEXT
    );
    
    CREATE TABLE check_depends (
        db TEXT,
        package TEXT,
        depend_package TEXT,
        version TEXT,
        comparator TEXT
    );
    
    CREATE TABLE opt_depends (
        db TEXT,
        package TEXT,
        depend_package TEXT,
        version TEXT,
        comparator TEXT,
        description TEXT
    );
    
    CREATE TABLE conflicts (
        db TEXT,
        package TEXT,
        conflict_package TEXT,
        version TEXT,
        comparator TEXT
    );
    
    CREATE TABLE provides (
        db TEXT,
        package TEXT,
        provide_package TEXT,
        version TEXT,
        comparator TEXT
    );
    
    CREATE TABLE replaces (
        db TEXT,
        package TEXT,
        replace_package TEXT,
        version TEXT,
        comparator TEXT
    );
"""

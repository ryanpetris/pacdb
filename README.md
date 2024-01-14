# PACDB

PACDB is a simple program that reads Pacman sync databases and dumps the contents into a queryable SQLite database. Also included is a systemd path/service to generate the database when the sync databases are updated.

When run as root, the database will be created at /var/lib/pacdb/pacman.sqlite. Otherwise, the pacman.sqlite file will be written to the current directory.
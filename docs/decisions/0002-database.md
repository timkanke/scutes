---
ID: umd-whpool-0002
Status: Accepted
Date: 2023-08-04
Author: Tim Kanke <tkanke@umd.edu>

---

# Use two database types: `SQLite` for dev and `PostgreSQL` for test, QA, and prod

## Context

We need to decide which database(s) to use for Scutes. Django offically supports PostgreSQLQL, MariaDB, MySQL, Oracle, and SQLite.

## Decision Drivers

* Use databases that we already have experience using
* Be easy to integrate into our current development/production patterns
* Be straightforward to develop and maintain

## Considered Options

1. Use `SQLite` for dev and `PostgreSQL` for test, QA, and prod
2. Use `PostgreSQL` for dev, test, QA, and prod

## Decision

Chosen option: Use `SQLite` for dev and `PostgreSQL` for test, QA, and prod, because it provides the easiest setup for dev work and a robust database for production.

## Pros and Cons of the Options

### Use `SQLite` for dev and `PostgreSQL` for test, QA, and prod

* Good, because it provides ease of set up for dev environment
* Good, because it provides ease of deleting/creating new SQLite db for dev work
* Bad, because it will require two separate project/settings.py files

### Use `PostgreSQL` for dev, test, QA, and prod

* Good, because it requires only one project database settings
* Bad, because it requires dev environment to have a local PostgreSQL installation
* Bad, because it requires more effort to deleting/creating new db for dev work

# scutes

Item Processing Application for WHCA Pool Reports Collection

## Development Environment

See [docs/DevelopmentEnvironment.md](docs/DevelopmentEnvironment.md).

## CKEditor

See [docs/CKEditor.md](docs/CKEditor.md).

## Database Schema

![Database Schema](docs/images/db_schema.svg)

## Management Commands

All commands are ran in the src directory.

Load YAML test data

```zsh
./manage.py loaddata test_data
```

Load mbox file

```zsh
# load mbox
./manage.py load_mbox_data path/to/file.mbox 

# Load test mbox file
./manage.py load_mbox_data ../tests/processing/data/test.mbox 
```

Clean HTML

```zsh
./manage.py clean <batch_number>
```

Redact HTML

```zsh
./manage.py mark_redaction <batch_number>
```

Finalize Redactions

```zsh
./manage.py finalize_redactions <batch_number>
```

## Architecture Decision Documents

The architecture decision documents are:

* [ADR Template](docs/decisions/adr-template.md)
* [0001-record-architecture-decisions](docs/decisions/0001-record-architecture-decisions.md)
* [0002-database](docs/decisions/0002-database.md)
* [0003-CKEditor-installation](docs/decisions/0003-CKEditor-installation.md)

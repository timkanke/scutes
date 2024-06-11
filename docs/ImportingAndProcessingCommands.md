# Importing and Processing Commands

All commands are ran in the src directory.

Import batches

```zsh
# Imports mbox file(s), cleans HTML, and marks redactions from a directory
./manage.py import_process path/to/dir 
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

Export

```zsh
./manage.py export <batch_number> <output_directory>
```

# scutes

Scutes is a [Django]-based web application for processing and redaction of personal identification information the WHCA Pool Reports Collection

## Development Environment

For guidance on setting up a Scutes development environment on a local workstation see the following:

[docs/DevelopmentEnvironment.md](docs/DevelopmentEnvironment.md).

## CKEditor

Scutes uses [CKEditor], a WYSIWYG editor, for manual making of redactions and light editing of item message bodies. A [custom redaction plugin](https://github.com/timkanke/ckeditor5-redact-plugin) allows curators to mark text to be redacted or remove redacted text that the automated redaction script has previously marked.

See [docs/CKEditor.md](docs/CKEditor.md) for directions on how CKEditor was built and integrated into Scutes.

## CLI Commands

Guidance on running CLI commands for this application can be found in the following:

* [Starting the Webserver](docs/StartingTheWebserver.md)
* [Importing and Processing Commands](docs/DatabaseSchema.md)

## Additional Documentation

Additional documentation for this application is in the "docs/" subdirectory, including:

* [Architecture Decision Records](docs/ArchitectureDecisionRecords.md)
* [Database Schema](docs/DatabaseSchema.md)

[Django]: https://www.djangoproject.com/
[CKEditor]: https://ckeditor.com/

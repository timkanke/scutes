# scutes

Scutes is a [Django]-based web application for processing and redaction of personal identification information for the White House Correspondents' Association (WHCA) Pool Reports Collection.

The collection is publicly viewable on the [WHCA Pool Reports Collection] website.

For information about the WHCA and the collection processing workflow see the [WHCA Pool Reports Collection About Page].

## Development Environment

For guidance on setting up a Scutes development environment on a local workstation see the following:

[docs/DevelopmentEnvironment.md](docs/DevelopmentEnvironment.md).

## CKEditor

Scutes uses [CKEditor], a WYSIWYG editor, for manual marking redactions and light editing of item message bodies. A [custom redaction plugin](https://github.com/timkanke/ckeditor5-redact-plugin) allows curators to mark text to be redacted or remove redacted text that was marked by the automated redaction script.

See [docs/CKEditor.md](docs/CKEditor.md) for directions on how CKEditor was built and integrated into Scutes.

## CLI Commands

Guidance on running CLI commands for this application can be found in the following:

* [Starting the Webserver](docs/StartingTheWebserver.md)
* [Importing and Processing Commands](docs/ImportingAndProcessingCommands.md)

## Additional Documentation

Additional documentation for this application is in the "docs/" subdirectory, including:

* [Architecture Decision Records](docs/ArchitectureDecisionRecords.md)
* [Database Schema](docs/DatabaseSchema.md)

[Django]: https://www.djangoproject.com/
[CKEditor]: https://ckeditor.com/
[WHCA Pool Reports Collection]: https://whpool.lib.umd.edu/
[WHCA Pool Reports Collection About Page]: https://whpool.lib.umd.edu/about

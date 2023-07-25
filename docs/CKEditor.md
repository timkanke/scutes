# CKEditor Notes

## Basic Install via git

In project root:

```zsh
git clone https://github.com/hvlads/django-ckeditor-5.git
```

Move django_ckeditor_5 to src directory
Remove remaining cloned directory

Add "django_ckeditor_5" to INSTALLED_APPS in scutes/settings.py:

```python
INSTALLED_APPS = [
...
'django_ckeditor_5',
]
```

At the bottom of scutes/settings.py add:

```python
customColorPalette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple'
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
]

# CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
# CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage" # optional
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['paragraph', '|',
                    'outdent', 'indent', '|',
                    'bold', 'italic', 'link', 'underline', 'strikethrough',
                    'code', 'subscript', 'superscript', 'highlight', '|',
                    'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',
                    'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor',
                    'mediaEmbed', 'removeFormat', 'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', '|',
                        'imageStyle:alignLeft', 'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',
                        '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells','tableProperties', 'tableCellProperties'],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        },
        'htmlSupport': {
            'allow': [
                {'name': '/.*/', 'attributes': True, 'classes': True, 'styles': True}
            ]
        },
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}
```

django_ckeditor_5, run:
```yarn install```
```yarn run prod```

In src run:
```./manage collectstatic```

Add to processing/forms.py:

```python
from django_ckeditor_5.widgets import CKEditor5Widget

...
    class Meta:
        ...

        widgets = {
            "body": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }
```

Add to scutes/urls.py:

```python
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

...

urlpatterns = [
    ...
    
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Install pillow:
```pip install pillow```

Add pillow to pyproject.toml and requirements.txt

## Add redact plugin

In django_ckeditor_5 directory, run:
```yarn add github:timkanke/ckeditor5-redact```
```yarn run prod```

Add to django_ckeditor_5/static/django_ckeditor_5/src/ckeditor.js

```js
import { Redact } from '@ckeditor/ckeditor5-redact';

...

ClassicEditor.builtinPlugins = [

  Redact,

...
```

Check static/django_ckeditor_5/package.json for:

```json
"dependencies": {
...
"@ckeditor/ckeditor5-redact": "github:timkanke/ckeditor5-redact",
...
},
```

Add plugin to settings.py 'toolbar':

```python
...
        'toolbar': 'redact', '|', 'paragraph', '|',
                    'outdent', 'indent', '|',
                    
                    ...
```

### Install and build ckeditor

In django_ckeditor_5, run:

```yarn install```

```yarn run prod```

In src, run:

```./manage.py collectstatic```

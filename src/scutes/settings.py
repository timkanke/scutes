"""
Django 4.2.3 settings for scutes project.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/

Production checklist
https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
"""

import environ
import saml2
import saml2.saml

from django.core.management.commands.runserver import Command as runserver

from pathlib import Path


env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(Path(BASE_DIR) / '.env')

# False if not in os.environ because of casting above
DEBUG = env.bool('DEBUG', default=False)

# Export files that are created for testing before zip
KEEP_EXPORT_DIRECTORIES = env.bool('KEEP_EXPORT_DIRECTORIES', default=DEBUG)

# Raises Django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env('ALLOWED_HOSTS', cast=[str])
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS', cast=[str])

ALLOWED_HOSTS = env('ALLOWED_HOSTS', cast=[str])
runserver.default_port = env('SERVER_PORT')
runserver.default_addr = env('SERVER_HOST')

# Needed for Django Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'processing',
    'django_tables2',
    'django_filters',
    'django_bootstrap5',
    'django_ckeditor_5',
    'crispy_forms',
    'crispy_bootstrap5',
    'debug_toolbar',
    'djangosaml2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django_auto_logout.middleware.auto_logout',
]

AUTH_USER_MODEL = 'processing.User'

AUTO_LOGOUT = {
    'IDLE_TIME': env('IDLE_TIME', cast=int),
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
}


""" SAML Config """

MIDDLEWARE.append('djangosaml2.middleware.SamlSessionMiddleware')

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'scutes.authentication.ModifiedSaml2Backend',
)

# SameSite Cookies
# The storage linked to it is accessible by default at request.saml_session.
SAML_SESSION_COOKIE_NAME = 'saml_session'
# By default, djangosaml2 will set “SameSite=None” for the SAML session cookie.
SAML_SESSION_COOKIE_SAMESITE = env('SAML_SESSION_COOKIE_SAMESITE')
# Remember that in your browser “SameSite=None” attribute MUST also have the “Secure” attribute,
# which is required in order to use “SameSite=None”, otherwise the cookie will be blocked.
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', cast=bool)

# Default login path
LOGIN_URL = '/saml2/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Handling Post-Login Redirects
SAML_ALLOWED_HOSTS = env('SAML_ALLOWED_HOSTS', cast=[str])

SAML_DEFAULT_BINDING = saml2.BINDING_HTTP_POST
SAML_LOGOUT_REQUEST_PREFERRED_BINDING = saml2.BINDING_HTTP_POST
SAML_IGNORE_LOGOUT_ERRORS = True

# Users, attributes and account linking
SAML_CREATE_UNKNOWN_USER = True
SAML_ATTRIBUTE_MAPPING = {
    'uid': ('username',),
    'mail': ('email',),
    'givenName': ('first_name',),
    'urn:mace:umd.edu:sn': ('last_name',),
    'eduPersonEntitlement': ('process_entitlement',),
}

SAML_CONFIG = {
    # full path to the xmlsec1 binary programm
    'xmlsec_binary': env('XMLSEC_BINARY'),
    # your entity id, usually your subdomain plus the url to the metadata view
    'entityid': env('ENTITYID'),
    # directory with attribute mapping
    'attribute_map_dir': str(Path(BASE_DIR) / 'scutes' / 'attribute-maps'),
    # Permits to have attributes not configured in attribute-mappings
    # otherwise...without OID will be rejected
    'allow_unknown_attributes': True,
    # this block states what services we provide
    'service': {
        'sp': {
            'name': 'Scutes',
            'name_id_format': saml2.saml.NAMEID_FORMAT_TRANSIENT,
            # Define the authentication context
            'requested_authn_context': {
                'authn_context_class_ref': [
                    'urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport',
                    'urn:oasis:names:tc:SAML:2.0:ac:classes:TLSClient',
                ],
                'comparison': 'minimum',
            },
            'endpoints': {
                # url and binding to the assetion consumer service view
                # do not change the binding or service name
                'assertion_consumer_service': [
                    (env('ENDPOINT_ADDRESS') + '/saml2/acs/', saml2.BINDING_HTTP_POST),
                ],
                # url and binding to the single logout service view
                # do not change the binding or service name
                'single_logout_service': [
                    # Disable next two lines for HTTP_REDIRECT for IDP's that only support HTTP_POST. Ex. Okta:
                    (env('ENDPOINT_ADDRESS') + '/saml2/ls/', saml2.BINDING_HTTP_REDIRECT),
                    (env('ENDPOINT_ADDRESS') + '/saml2/ls/post', saml2.BINDING_HTTP_POST),
                ],
            },
            'signing_algorithm': saml2.xmldsig.SIG_RSA_SHA256,
            'digest_algorithm': saml2.xmldsig.DIGEST_SHA256,
            # Mandates that the identity provider MUST authenticate the
            # presenter directly rather than rely on a previous security context.
            'force_authn': False,
            # Enable AllowCreate in NameIDPolicy.
            'name_id_format_allow_create': False,
            # attributes that this project need to identify a user
            'required_attributes': ['givenName', 'sn', 'mail', 'eduPersonEntitlement'],
            # attributes that may be useful to have but not required
            'optional_attributes': ['eduPersonAffiliation'],
            'want_response_signed': False,
            'authn_requests_signed': True,
            'logout_requests_signed': True,
            # Indicates that Authentication Responses to this SP must
            # be signed. If set to True, the SP will not consume
            # any SAML Responses that are not signed.
            'want_assertions_signed': False,
            'only_use_keys_in_metadata': True,
            # When set to true, the SP will consume unsolicited SAML
            # Responses, i.e. SAML Responses for which it has not sent
            # a respective SAML Authentication Request.
            'allow_unsolicited': True,
            # in this section the list of IdPs we talk to are defined
            # This is not mandatory! All the IdP available in the metadata will be considered instead.
            'idp': {
                # we do not need a WAYF service since there is
                # only an IdP defined here. This IdP should be
                # present in our metadata
                # the keys of this dictionary are entity ids
                'https://shib.idm.umd.edu/shibboleth-idp/shibboleth': {
                    'single_sign_on_service': {
                        saml2.BINDING_HTTP_POST: 'https://shib.idm.umd.edu/shibboleth-idp/profile/SAML2/POST/SSO',
                    },
                    'single_logout_service': {
                        saml2.BINDING_HTTP_REDIRECT: 'https://shib.idm.umd.edu/shibboleth-idp/profile/Logout',
                    },
                },
            },
        },
    },
    # where the remote metadata is stored, local, remote or mdq server.
    'metadata': {
        'remote': [
            {'url': 'https://shib.idm.umd.edu/shibboleth-idp/shibboleth'},
        ],
    },
    # set to 1 to output debugging information
    'debug': 1,
    # Signing
    'key_file': env('KEY_FILE'),  # private part
    'cert_file': env('CERT_FILE'),  # public part
    # Encryption
    'encryption_keypairs': [
        {
            'key_file': env('KEY_FILE'),  # private part
            'cert_file': env('CERT_FILE'),  # public part
        }
    ],
}

""" END SAML CONFIG """

ROOT_URLCONF = 'scutes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path(BASE_DIR) / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_auto_logout.context_processors.auto_logout_client',
            ],
            'libraries': {
                'common_extras': 'scutes.templatetags.common_extras',
            },
        },
    },
]

DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap5.html'

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

WSGI_APPLICATION = 'scutes.wsgi.application'

# Databases
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

# Log any emails sent to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = env('STATIC_URL')
STATIC_ROOT = env('STATIC_ROOT')
MEDIA_URL = env('MEDIA_URL')
MEDIA_ROOT = env('MEDIA_ROOT')
EXPORT_PATH = Path(MEDIA_ROOT, 'export')


# Logging
LOGGING = {
    'version': 1,  # the dictConfig format version
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': env('LOGGING_LEVEL'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL'),
            'propagate': False,
        },
    },
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

customColorPalette = [
    {'color': 'hsl(4, 90%, 58%)', 'label': 'Red'},
    {'color': 'hsl(340, 82%, 52%)', 'label': 'Pink'},
    {'color': 'hsl(291, 64%, 42%)', 'label': 'Purple'},
    {'color': 'hsl(262, 52%, 47%)', 'label': 'Deep Purple'},
    {'color': 'hsl(231, 48%, 48%)', 'label': 'Indigo'},
    {'color': 'hsl(207, 90%, 54%)', 'label': 'Blue'},
]

# CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
# CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage" # optional
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading',
            '|',
            'bold',
            'italic',
            'link',
            'bulletedList',
            'numberedList',
            'blockQuote',
            'imageUpload',
        ],
    },
    'extends': {
        'blockToolbar': [
            'paragraph',
            'heading1',
            'heading2',
            'heading3',
            '|',
            'bulletedList',
            'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': [
            'paragraph',
            'redact',
            '|',
            'outdent',
            'indent',
            '|',
            'bold',
            'italic',
            'link',
            'underline',
            'strikethrough',
            '|',
            # 'code', 'subscript', 'superscript', 'highlight', '|',
            # 'codeBlock',
            'sourceEditing',
            # 'insertImage',
            # 'bulletedList', 'numberedList', 'todoList', '|',
            # 'blockQuote', 'imageUpload', '|',
            # 'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor',
            # 'mediaEmbed', 'removeFormat', 'insertTable',
        ],
        'image': {
            'toolbar': [
                'imageTextAlternative',
                '|',
                'imageStyle:alignLeft',
                'imageStyle:alignRight',
                'imageStyle:alignCenter',
                'imageStyle:side',
                '|',
            ],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ],
        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties'],
            'tableProperties': {'borderColors': customColorPalette, 'backgroundColors': customColorPalette},
            'tableCellProperties': {'borderColors': customColorPalette, 'backgroundColors': customColorPalette},
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'},
            ]
        },
        'htmlSupport': {'allow': [{'name': '/.*/', 'attributes': True, 'classes': True, 'styles': True}]},
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    },
}

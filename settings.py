"""
Django settings for battery_mgmt project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured
from celery.task.schedules import crontab

import saml2  # noqa
from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED  # noqa
from saml2.sigver import get_xmlsec_binary  # noqa

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=0))
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB_NUM = os.environ.get("REDIS_DB_NUM")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_LOG_GROUP = os.environ.get('AWS_LOG_GROUP')
USE_S3 = os.getenv('USE_S3') == 'TRUE'

ALLOWED_HOSTS = ['*'] # Need to investigate this 


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider', # OAuth2
    'corsheaders',
    'rest_framework', # API
    'batteries.apps.BatteriesConfig',
    'entities.apps.EntitiesConfig',
    'filestore.apps.FilestoreConfig',
    'loads.apps.LoadsConfig',
    'orgs.apps.OrgsConfig',
    'roles.apps.RolesConfig',
    'stats.apps.StatsConfig',
    'users.apps.UsersConfig',
    'access_requests.apps.AccessRequestsConfig',
    'notifications.apps.NotificationsConfig',
    'redirect.apps.RedirectConfig',
    'unit_tests.apps.UnitTestsConfig',
    'vehicles.apps.VehiclesConfig',
    'init',
    'djangosaml2idp',
    'drf_yasg',
    'phonenumber_field',
    'django_filters',
    'django_extensions',
    'middlewares',
    'django_otp',
    'django_otp.plugins.otp_email',
    'sslserver',
    'channels',
    'daphne',
    'zoho',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'middlewares.log_4xx_middleware.log_4xx_middleware',
    # 'middlewares.whitelist_middleware.whitelist_middleware',
]

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication', # To keep the Browsable API
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DATETIME_INPUT_FORMATS': ['iso-8601', '%Y-%m-%dT%H:%M:%S.%fZ'],
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # To keep the Browsable API
    'oauth2_provider.backends.OAuth2Backend',
)

OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'

OAUTH2_PROVIDER = {
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
    'ACCESS_TOKEN_EXPIRE_SECONDS': 60 * 60 * 24 * 14,
}

ROOT_URLCONF = 'battery_mgmt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://"+REDIS_HOST+":"+REDIS_PORT+"/"+REDIS_DB_NUM,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        }
    }
}

WSGI_APPLICATION = 'battery_mgmt.wsgi.application'


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('POSTGRES_DB'),
        'USER': get_env_variable('POSTGRES_USER'),
        'PASSWORD': get_env_variable('POSTGRES_PASSWORD'),
        'HOST': get_env_variable('DB_HOST'),
        'PORT': get_env_variable('DB_PORT'),
    }
}

AUTH_USER_MODEL = 'users.User'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

BASE_URL = get_env_variable('BASE_URL')

BROKER_URL = 'redis://'+REDIS_HOST+':'+REDIS_PORT
CELERY_RESULT_BACKEND = 'redis://'+REDIS_HOST+':'+REDIS_PORT
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS=()
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERYBEAT_SCHEDULE = {
    # 'create_batteries_data_filestores_once_a_day': {
    #     'task': 'batteries.tasks.create_batteries_data_filestores',
    #     'schedule': crontab(hour='23', minute='59')
    #     },
    # 'create_logs_filestore_once_a_day': {
    #     'task': 'battery_mgmt.tasks.create_filestore_for_logs',
    #     'schedule': crontab(hour='23', minute='59')
    #     },
    'export_daily_logs_from_clouwatch_to_s3': {
        'task': 'battery_mgmt.tasks.export_logs_once_a_day_from_cloudwatch_to_s3',
        'schedule': crontab(hour='23', minute='20')
        },
    'delete_compressed_log_files': {
        'task': 'battery_mgmt.tasks.delete_compressed_log_files',
        'schedule': crontab(hour='23', minute='59', day_of_week='sun')
        },
    'delete_outdated_battery_data': {
        'task': 'batteries.tasks.delete_batteries_data_older_than_one_month',
        'schedule': crontab(hour='23', minute='59')
        },
    # 'generate_freshworld_daily_report': {
    #     'task': 'battery_mgmt.tasks.generate_freshworld_daily_report',
    #     'schedule': crontab(hour='8', minute='00')
    #     },
    'daily_add_derived_load_data_columns_for_mantis': {
        'task': 'loads.tasks.daily_add_derived_load_data_columns_for_mantis',
        'schedule': crontab(hour='1', minute='00')
        },
    }

EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 465
SENDER_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


if USE_S3:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_DEFAULT_ACL = None

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "files_for_static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Settings for swagger api generation
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'LOGIN_URL': '/acconts/login/',
    'LOGOUT_URL': '/accounts/logout/',
    'OPERATIONS_SORTER': 'method',
}

ADMINS = [('Orxa Admin', 'sysadmin@orxaenergies.com')]
LOGGING_CONFIG = 'logging.config.dictConfig'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Include the default Django email handler for errors
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'include_html': True,
        },
        # Handler to log 'ERROR' to a file.
        'error_logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': BASE_DIR + '/logs/django-logs.log',
            'level': 'ERROR'
        },
    },
    'loggers': {
        # Django configuration to email unhandled exceptions
        'django.request': {
            'handlers': ['mail_admins', 'error_logfile'],
            'propagate': True,
        },
    },
}

TEST_SKIP_MIGRATIONS = os.environ.get('TEST_SKIP_MIGRATIONS')
if TEST_SKIP_MIGRATIONS:
    class DisableMigrations(object):

        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()

GOOGLE_RECAPTCHA_SITE_KEY = get_env_variable('GOOGLE_RECAPTCHA_SITE_KEY')

ORXA_SUPER_ADMIN_EMAIL = get_env_variable('ORXA_SUPER_ADMIN_EMAIL')
ORXA_SUPER_ADMIN_PASSWORD = get_env_variable('ORXA_SUPER_ADMIN_PASSWORD')
ORXA_SUPER_ADMIN_MOBILE_NUMBER = get_env_variable('ORXA_SUPER_ADMIN_MOBILE_NUMBER')
ORXA_SUPER_ADMIN_FIRST_NAME = get_env_variable('ORXA_SUPER_ADMIN_FIRST_NAME')
ORXA_SUPER_ADMIN_LAST_NAME = get_env_variable('ORXA_SUPER_ADMIN_LAST_NAME')

SYS_ADMIN_EMAIL = get_env_variable('SYS_ADMIN_EMAIL')
SYS_ADMIN_PASSWORD = get_env_variable('SYS_ADMIN_PASSWORD')

ASGI_APPLICATION = "battery_mgmt.asgi.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

ZOHO_ORXA_BATTERY_MGMT_SERVER_CLIENT = {
    'client_id': os.environ.get("ZOHO_ORXA_BATTERY_MGMT_SERVER_CLIENT_ID"),
    'client_secret': os.environ.get("ZOHO_ORXA_BATTERY_MGMT_SERVER_CLIENT_SECRET"),
    'redirect_uri': os.environ.get("ZOHO_ORXA_BATTERY_MGMT_SERVER_CLIENT_REDIRECT_URI"),
}

ZOHO_DESKS_ORXA_BATTERY_MGMT_SERVER_CLIENT = {
    'refresh_token': os.environ.get("ZOHO_DESKS_ORXA_BATTERY_MGMT_SERVER_CLIENT_REFRESH_TOKEN"),
    'scope': os.environ.get("ZOHO_DESKS_ORXA_BATTERY_MGMT_SERVER_CLIENT_SCOPE"),
}

ZOHO_DESKS_ORXA_BATTERY_MGMT_SERVER_CLIENT.update(ZOHO_ORXA_BATTERY_MGMT_SERVER_CLIENT)

ZOHO_DESKS_ORXA_ENERGIES_ORGANISATION_ID = os.environ.get("ZOHO_DESKS_ORXA_ENERGIES_ORGANISATION_ID")
ZOHO_DESKS_ORXA_ENERGIES_DEPARTMENT_ID = os.environ.get("ZOHO_DESKS_ORXA_ENERGIES_DEPARTMENT_ID")

ZOHO_CAMPAIGNS_ORXA_BATTERY_MGMT_SERVER_CLIENT = {
    'refresh_token': os.environ.get("ZOHO_CAMPAIGNS_ORXA_BATTERY_MGMT_SERVER_CLIENT_REFRESH_TOKEN"),
    'scope': os.environ.get("ZOHO_CAMPAIGNS_ORXA_BATTERY_MGMT_SERVER_CLIENT_SCOPE"),
}

ZOHO_CAMPAIGNS_ORXA_BATTERY_MGMT_SERVER_CLIENT.update(ZOHO_ORXA_BATTERY_MGMT_SERVER_CLIENT)
ZOHO_ASAP_ADD_ON_SECRET_KEY = os.environ.get("ZOHO_ASAP_ADD_ON_SECRET_KEY")

# djangisaml2idp config for SAML identity provider
SAML_IDP_CONFIG = {
    'debug': DEBUG,
    'xmlsec_binary': get_xmlsec_binary(['/opt/local/bin', '/usr/bin/xmlsec1']),
    'entityid': f'{BASE_URL}/idp/metadata/',
    'description': 'Example IdP setup',

    'service': {
        'idp': {
            'name': 'Django localhost IdP',
            'endpoints': {
                'single_sign_on_service': [
                    (f'{BASE_URL}/idp/sso/post/', saml2.BINDING_HTTP_POST),
                    (f'{BASE_URL}/idp/sso/redirect/', saml2.BINDING_HTTP_REDIRECT),
                ],
                "single_logout_service": [
                    (f"{BASE_URL}/idp/slo/post/", saml2.BINDING_HTTP_POST),
                    (f"{BASE_URL}/idp/slo/redirect/", saml2.BINDING_HTTP_REDIRECT)
                ],
            },
            'name_id_format': [NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED],
            'sign_response': True,
            'sign_assertion': True,
            'want_authn_requests_signed': True,
        },
    },

    # Signing
    'key_file': os.path.join(BASE_DIR, 'battery_mgmt', 'certificates', 'private.key'),
    'cert_file': os.path.join(BASE_DIR, 'battery_mgmt', 'certificates', 'public.cert'),
    # Encryption
    'encryption_keypairs': [{
        'key_file': os.path.join(BASE_DIR, 'battery_mgmt', 'certificates', 'private.key'),
        'cert_file': os.path.join(BASE_DIR, 'battery_mgmt', 'certificates', 'public.cert'),
    }],
    'valid_for': 365 * 24,
}


SAML_AUTHN_SIGN_ALG = saml2.xmldsig.SIG_RSA_SHA256
SAML_AUTHN_DIGEST_ALG = saml2.xmldsig.DIGEST_SHA256
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

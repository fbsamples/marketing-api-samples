# Copyright (c) 2016-present, Facebook, Inc. All rights reserved.
#
# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.
#
# As with any software that integrates with the Facebook platform, your use of
# this software is subject to the Facebook Developer Principles and Policies
# [http://developers.facebook.com/policy/]. This copyright notice shall be
# included in all copies or substantial portions of the software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

BASE_DIR = os.path.dirname(__file__)
MUSE_ROOT_DIR = os.path.normpath(os.path.join(BASE_DIR, '..'))

# import env variables
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')

# setup muse mode variable and wrapper
MUSE_MODE = 'dev'


def IS_RELEASE():
    return MUSE_MODE == 'release'


def IS_TEST():
    return MUSE_MODE == 'test'


def IS_DEV():
    return MUSE_MODE == 'dev'


# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrapform',
    'sslserver',

    'security',
    'common',
    'common_templates',
    'components',
    'samples',
    'dash',
)

MIDDLEWARE_CLASSES = (
    'security.middleware.SslRedirect',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(MUSE_ROOT_DIR, 'common_templates'),
    os.path.join(MUSE_ROOT_DIR, 'samples/templates/samples'),
    os.path.join(MUSE_ROOT_DIR, 'dash/templates/dash'),
)

ROOT_URLCONF = 'muse.urls'

WSGI_APPLICATION = 'muse.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# muse config
LOGIN_URL = '/auth/login'
AUTHENTICATION_BACKENDS = (
    'security.models.FBAuthBackend',
)
AUTH_USER_MODEL = 'security.FBUser'
AUTH_BACKEND = 'security.models.FBAuthBackend'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django_settings_export.settings_export',
)

LOG_LEVEL = 'DEBUG'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
                '%(levelname)s %(asctime)s %(pathname)s %(lineno)s %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(MUSE_ROOT_DIR, 'muse.log')
        },
    },
    'loggers': {
        'security': {
            'handlers': ['default'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'common': {
            'handlers': ['default'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'samples': {
            'handlers': ['default'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'dash': {
            'handlers': ['default'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    },
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENABLE_DASH = True
TEMPLATE_DEBUG = True

DOC_TEMPLATE_DIR = os.path.join(MUSE_ROOT_DIR, 'common/doctemplates/')

STATIC_ROOT = os.path.abspath(os.path.join(MUSE_ROOT_DIR, 'staticfiles'))
STATICFILES_DIRS = (
    os.path.join(MUSE_ROOT_DIR, 'common', 'static'),
    os.path.join(MUSE_ROOT_DIR, 'components', 'static'),
    os.path.join(MUSE_ROOT_DIR, 'samples', 'static'),
)
STATIC_URL = '/static/'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3h5ehth8n9on9&m64cyb-2(ny%x43p3x5v()vydhp1=o33u)w^^+&khjk3jh5rh'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(MUSE_ROOT_DIR, 'db.sqlite3'),
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 3600  # 1 hr
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# export facebook app id for templates
SETTINGS_EXPORT = [
    'FACEBOOK_APP_ID',
]

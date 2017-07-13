# Required to define a secret key
SECRET_KEY = 'fake-key'

# We also need the sessions app, staticfiles (used in templates), and thumber itself installed
INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'tests',
    'thumber'
]

# Need a DB (use sqlite in memory) for storing models
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

# Load our test-specific url conf
ROOT_URLCONF = 'tests.root_urls'

# We need the session middlewre, since it's used by thumber
MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
]

# Must specify STATIC_URL if installing staticfiles app
STATIC_URL = '/static/'

# We don't want to a DB for our sessions, just use the filesystem
SESSION_ENGINE = "django.contrib.sessions.backends.file"

# Add the templates dir as this dir (so that example.html can be found)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

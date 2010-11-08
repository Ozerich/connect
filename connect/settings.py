STORAGE_PATH = '/home/ozerich/Work/connect/media/storage'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Eugeny Pankov', 'john.pankov@gmail.com'),
    ('Vitaly Ozerski', 'ozicoder@gmail.com')
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bsuir',
        'USER': 'root',
        'PASSWORD': 'admin',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Minsk'
LANGUAGE_CODE = 'ru-RU'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'ah+-4$xr!@pg04p5ekdivni8-b&9)u)z82vh#^zesrcyh7x95&'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
)

ROOT_URLCONF = 'connect.urls'

TEMPLATE_DIRS = (
    '/home/ozerich/work/connect/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'main',
)

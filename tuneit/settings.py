import os
from pathlib import Path
import pymysql
pymysql.install_as_MySQLdb()

#Base dir finds proj dir 
BASE_DIR = Path(__file__).resolve().parent.parent 
ON_VERCEL = os.environ.get('VERCEL') == '1'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if ON_VERCEL:
        raise RuntimeError('Set DJANGO_SECRET_KEY in the Vercel project environment.')
    SECRET_KEY = 'local-development-only-change-me'
DEBUG = os.environ.get('DJANGO_DEBUG', '0' if ON_VERCEL else '1') == '1'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_HOSTS.extend(
    host.strip()
    for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
    if host.strip()
)
if ON_VERCEL:
    ALLOWED_HOSTS.append('.vercel.app')
#Installed apps registers django applications 
INSTALLED_APPS = ['django.contrib.contenttypes', 'django.contrib.staticfiles', 'music'] 
#Middleware Runs request and response processing layers.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]
ROOT_URLCONF = 'tuneit.urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request']}}]
#If MYSQL_DATABASE exists, Django uses MySQL.Otherwise, Django uses SQLite
if os.environ.get('MYSQL_DATABASE'):
    import pymysql

    pymysql.install_as_MySQLdb()
    DATABASES = {'default': {'ENGINE':'django.db.backends.mysql','NAME':os.environ['MYSQL_DATABASE'], 'USER':os.environ.get('MYSQL_USER','root'),'PASSWORD':os.environ.get('MYSQL_PASSWORD',''),'HOST':os.environ.get('MYSQL_HOST','127.0.0.1'),'PORT':os.environ.get('MYSQL_PORT','3306')}}
else:
    if ON_VERCEL:
        raise RuntimeError(
            'Set MYSQL_DATABASE and the other MYSQL_* variables in Vercel; '
            'serverless SQLite storage is not persistent.'
        )
    DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR / 'db.sqlite3'}}
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

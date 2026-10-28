import os
from pathlib import Path
#Base dir finds proj dir 
BASE_DIR = Path(__file__).resolve().parent.parent 
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'local-development-only-change-me')
DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
#Installed apps registers django applications 
INSTALLED_APPS = ['django.contrib.contenttypes', 'django.contrib.staticfiles', 'music'] 
#Middleware Runs request and response processing layers.
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware'] 
ROOT_URLCONF = 'tuneit.urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request']}}]
#If MYSQL_DATABASE exists, Django uses MySQL.Otherwise, Django uses SQLite
if os.environ.get('MYSQL_DATABASE'):
    DATABASES = {'default': {'ENGINE':'django.db.backends.mysql','NAME':os.environ['MYSQL_DATABASE'], 'USER':os.environ.get('MYSQL_USER','root'),'PASSWORD':os.environ.get('MYSQL_PASSWORD',''),'HOST':os.environ.get('MYSQL_HOST','127.0.0.1'),'PORT':os.environ.get('MYSQL_PORT','3306')}}
else:
    DATABASES = {'default': {'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR / 'db.sqlite3'}}
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

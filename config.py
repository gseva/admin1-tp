import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = '\2\1thisismyscretkey\1\2\e\y\y\h'


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#SQLALCHEMY_DATABASE_URI = 'mysql://myapp@localhost/myapp'

BABEL_DEFAULT_LOCALE = 'en'

LANGUAGES = {
    # 'es': {'flag': 'es', 'name': 'Spanish'},
    'en': {'flag':'gb', 'name':'English'},
#     'pt': {'flag':'pt', 'name':'Portuguese'},
#     'de': {'flag':'de', 'name':'German'},
#     'zh': {'flag':'cn', 'name':'Chinese'},
#     'ru': {'flag':'ru', 'name':'Russian'}
}


#------------------------------
# GLOBALS FOR GENERAL APP's
#------------------------------
UPLOAD_FOLDER = basedir + '/app/static/uploads/'
IMG_UPLOAD_FOLDER = basedir + '/app/static/uploads/'
IMG_UPLOAD_URL = '/static/uploads/'
IMG_SIZE = (150,150,True)
AUTH_TYPE = 1
AUTH_ROLE_ADMIN = 'Admin'
AUTH_ROLE_PUBLIC = 'Public'
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = 'Client'
# RECAPTCHA_PUBLIC_KEY = 'set google public key'
# RECAPTCHA_PRIVATE_KEY = 'set google private key'
RECAPTCHA_DISABLE = True
APP_NAME = 'Grupo 3 - Proyecto'
APP_ICON = 'static/img/logo.png'
#APP_THEME = ''                  # default
#APP_THEME = 'cerulean.css'      # COOL
#APP_THEME = 'amelia.css'
APP_THEME = 'cosmo.css'
#APP_THEME = 'cyborg.css'       # COOL
#APP_THEME = 'flatly.css'
#APP_THEME = 'journal.css'
#APP_THEME = 'readable.css'
#APP_THEME = 'simplex.css'
#APP_THEME = 'slate.css'          # COOL
#APP_THEME = 'spacelab.css'      # NICE
#APP_THEME = 'united.css'

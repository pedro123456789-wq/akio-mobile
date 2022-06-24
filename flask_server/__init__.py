from os.path import isfile

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate


SQLALCHEMY_TRACK_MODIFICATIONS = True
app = Flask(__name__)

app.config['SECRET_KEY'] = 'test_key' #change in production
app.config['JSON_SORT_KEYS'] = False
app.config['ENV'] = 'development'

isDevMode = app.config['ENV'] == 'development'

if isDevMode:
    dbPath = 'test.db'
else:
    dbPath = 'production.db'
    cors = CORS(app, supports_credentials = True)

createNewDb = not isfile(f'flask_server/{dbPath}') 
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{dbPath}'

db = SQLAlchemy(app)
migrations = Migrate(app, db)
encryptionHandler = Bcrypt()

from flask_server import models 

if createNewDb:
    print('Creating new database')
    db.create_all()
    # populate db with default admin account, colours and sizes

from flask_server import views 

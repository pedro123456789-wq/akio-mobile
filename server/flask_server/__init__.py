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
app.config['DEBUG'] = True if app.config['ENV'] == 'development' else False 
isDevMode = app.config['ENV'] == 'development'

if isDevMode:
    db_path = 'test.db'
else:
    db_path = 'production.db'
    
cors = CORS(app, supports_credentials = True)
create_new_db = not isfile(f'flask_server/{db_path}')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)
migrations = Migrate(app, db)
encryption_handler = Bcrypt()

from flask_server import models 

if create_new_db:
    print('Creating new database')
    db.create_all()


from flask_server import views 

from pathlib import Path
from os.path import isfile

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate

SQLALCHEMY_TRACK_MODIFICATIONS = True
app = Flask(__name__)

app.config['SECRET_KEY'] = 'test_key'  # change in production
app.config['JSON_SORT_KEYS'] = False
app.config['ENV'] = 'development'
app.config['DEBUG'] = True if app.config['ENV'] == 'development' else False
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # To suppress the warning. Apparently it is slower to hjave it enabled.
isDevMode = app.config['ENV'] == 'development'

if isDevMode:
    db_path = 'test.db'
else:
    db_path = 'production.db'

cors = CORS(app, supports_credentials=True)

print("Checking path for database: ", end="")
print(Path(f'{str(Path(__file__).as_posix())}/../flask_server/{db_path}').resolve())
create_new_db = not isfile(Path(f'{str(Path(__file__).as_posix())}/../{db_path}').resolve())
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)
migrations = Migrate(app, db)
encryption_handler = Bcrypt()

from flask_server import models

if create_new_db:
    from .models import User

    print('Creating new database')
    db.create_all()
    # Create admin account.
    with app.app_context():
        admin_account = User(username="admin",
                             hashed_password=encryption_handler.generate_password_hash(app.config["SECRET_KEY"]).decode(
                                 "utf-8"),
                             is_admin=True)
        db.session.add(admin_account)
        db.session.commit()

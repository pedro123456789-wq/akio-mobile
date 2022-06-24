from flask_server import app, db

@app.route('/api')
def home():
    return 'api running...'


@app.route('/login')
def login():
    pass 


@app.route('/sign-in')
def signIn():
    pass

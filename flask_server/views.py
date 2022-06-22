from flask_server import app, db

@app.route('/api')
def home():
    return 'api running...'

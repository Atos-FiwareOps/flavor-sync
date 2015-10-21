from flavorsync import config

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    if app.config['TESTING']:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DB_TEST_URI']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
    
    db.init_app(app)
    db.create_all()
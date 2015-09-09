from flavorsync import config

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
    db.init_app(app)
    db.create_all()
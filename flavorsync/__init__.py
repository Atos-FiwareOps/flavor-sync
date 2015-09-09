from flask import Flask

app = Flask(__name__)

from flavorsync.database import init_db

import flavorsync.views

with app.app_context():
    init_db(app)
from flavorsync import app
from flavorsync.database import init_db
import flavorsync.views

with app.app_context():
    init_db(app)

app.run(debug=True)
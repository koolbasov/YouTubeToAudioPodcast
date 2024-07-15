from webapp import db, create_app
from webapp.languages_for_db import languages, add_languages_to_db

db.create_all(app=create_app())
app = create_app()
db.init_app(app)

with app.app_context():
    add_languages_to_db(languages)

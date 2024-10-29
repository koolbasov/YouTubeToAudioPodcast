from webapp import db, create_app
from webapp.languages_for_db import languages, add_languages_to_db

app = create_app()
with app.app_context():
    db.create_all()
    add_languages_to_db(languages)

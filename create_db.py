from webapp import db, create_app
from webapp.utils import add_languages_to_db
from webapp.config import LANGUAGES

app = create_app()
with app.app_context():
    db.create_all()
    add_languages_to_db(LANGUAGES)

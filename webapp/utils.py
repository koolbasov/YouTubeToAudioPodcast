from urllib.parse import urlparse, urljoin
from flask import request

from webapp.podcast.models import db, Language


def add_languages_to_db(languages):
    for language_name, short_name in languages.items():
        language_exists = Language.query.filter(Language.identifier == short_name).count()
        if not language_exists:
            new_language = Language(language=language_name, identifier=short_name)
            db.session.add(new_language)
            db.session.commit()


def languages_for_form():
    languages_list = Language.query.all()
    languages_set = []
    for language in languages_list:
        languages_set.append((language.id, language.language))
    return languages_set


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get("next"), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

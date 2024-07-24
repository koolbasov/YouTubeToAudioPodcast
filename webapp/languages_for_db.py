from webapp.models import db, Language

languages = {
    "Chinese (Simplified)":  "zh-cn",
    "English":  "en",
    "French":  "fr",
    "German":  "de",
    "Italian":  "it",
    "Russian":  "ru",
    "Spanish":  "es",
}


def add_languages_to_db(languages):
    for language_name, short_name in languages.items():
        language_exists = Language.query.filter(
            Language.identifier == short_name).count()
        if not language_exists:
            new_language = Language(
                language=language_name, identifier=short_name)
            db.session.add(new_language)
            db.session.commit()


def languages_for_form():
    languages_list = Language.query.all()
    languages_set = []
    for language in languages_list:
        languages_set.append((language.id, language.language))
    return languages_set

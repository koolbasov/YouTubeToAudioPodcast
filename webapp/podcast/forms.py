from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError

from webapp.podcast.parser.get_xml_html import is_valid_playlist


class DownloadFeedForm(FlaskForm):
    feed_link = StringField(
        "Вставьте ссылку для скачивания", validators=[DataRequired()], render_kw={"class": "form-control"}
    )
    language = SelectField("Выберите язык", validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField("Загрузить плейлист", render_kw={"class": "btn btn-warning"})

    def validate_feed_link(self, feed_link: StringField) -> ValidationError:
        is_youtube = "youtu.be" in feed_link.data or "youtube.com" in feed_link.data
        is_playlist = "playlist" in feed_link.data
        if not is_youtube:
            raise ValidationError("Похоже это не ссылка на YouTube")
        if not is_playlist:
            raise ValidationError("Похоже это не плейлист")
        if not is_valid_playlist(feed_link.data):
            raise ValidationError("Похоже вы пытаетесь загрузить private плейлист")

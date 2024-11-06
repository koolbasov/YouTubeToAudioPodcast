from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from webapp.db import db
from webapp.podcast.models import Feed, Podcast
from webapp.podcast.parser.create_feed import feed_generator
from webapp.podcast.parser.get_xml_html import get_html_from_youtube
from webapp.podcast.parser.parser_to_db import parse_fields_for_data_base
from webapp.utils import languages_for_form
from webapp.podcast.forms import DownloadFeedForm

blueprint = Blueprint("podcast", __name__)


@blueprint.route("/home")
@login_required
def main():
    languages_set = languages_for_form()
    form = DownloadFeedForm()
    form.language.choices = languages_set
    title = "YouTubeToAudioPodcast | подкасты"
    playlists = Feed.query.filter_by(user_id=current_user.id).all()
    rss_links = []
    for playlist in playlists:
        link = feed_generator(playlist.id)
        rss_links.append(link)
    return render_template(
        "podcast/mainpage.html", page_title=title, playlists=playlists, rss_links=rss_links, form=form
    )


@blueprint.route("/delete_playlist/<int:playlist_id>")
@login_required
def delete_playlist(playlist_id):
    playlist = Feed.query.filter_by(id=playlist_id).first()
    flash(f"Вы удалили плейлист  {playlist.feed_title}")
    db.session.delete(playlist)
    db.session.commit()
    return redirect(url_for("podcast.main"))


@blueprint.route("/download", methods=["POST"])
@login_required
def process_download():
    languages_set = languages_for_form()
    form = DownloadFeedForm()
    form.language.choices = languages_set
    if form.validate_on_submit():
        feed_link_data = form.feed_link.data
        language_data = form.language.data
        user_id_data = current_user.id
        playlist_xml, playlist_html, playlist_id = get_html_from_youtube(feed_link_data)
        flash("Ваш плейлист загружен")
        parse_fields_for_data_base(
            feed_link_data, playlist_xml, playlist_html, playlist_id, language_data, user_id_data
        )
        return redirect(url_for("podcast.main"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле "{getattr(form, field).label.text}": {error}')
        return redirect(url_for("podcast.main"))


@blueprint.route("/podcast/<int:podcast_id>")
def podcast(podcast_id):
    title = "YouTubeToAudioPodcast | подкаст"
    try:
        my_podcasts = Podcast.query.filter(Podcast.feed_id == podcast_id).all()
        feed_title = Feed.query.filter(Feed.id == podcast_id).first().feed_title
        rss_link = feed_generator(podcast_id)
        return render_template(
            "podcast/podcast.html", page_title=title, feed_title=feed_title, podcasts=my_podcasts, rss_link=rss_link
        )
    except AttributeError:
        flash("Такого подкаста еще не загружено или он был удален")
        return redirect(url_for("podcast.main"))


@blueprint.route("/delete_podcast/<int:podcast_id>", methods=["GET"])
@login_required
def delete_podcast(podcast_id):
    podcast_to_delete = Podcast.query.filter_by(id=podcast_id).first()
    playlist_id = podcast_to_delete.feed_id
    flash(f"Вы удалили подкаст: {podcast_to_delete.podcast_title}")
    db.session.delete(podcast_to_delete)
    db.session.commit()
    return redirect(url_for("podcast.podcast", podcast_id=playlist_id))

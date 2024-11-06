from flask import Blueprint, render_template
from flask_login import current_user

from webapp.admin.decorators import admin_required

blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@blueprint.route("/")
@admin_required
def admin():
    if current_user.is_admin:
        title = "YouTubeToAudioPodcast | Панель управления"
        return render_template("admin/admin.html", page_title=title)
    return "У вас нет прав администратора"

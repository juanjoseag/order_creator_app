from io import BytesIO
from flask import Blueprint, send_file
from app.models import Image

bp = Blueprint("image", __name__)


@bp.route("/<int:image_id>")
def image(image_id):
    image = Image.query.get_or_404(image_id)
    return send_file(BytesIO(image.image), mimetype=image.mimetype)

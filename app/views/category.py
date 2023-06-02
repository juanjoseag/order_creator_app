from flask import Blueprint, request, render_template, redirect, url_for
from app.models import Category, Product

bp = Blueprint("category", __name__)


@bp.route("/")
def index():
    category = Category.query.first()
    return redirect(url_for("category.category", category_id=category.id))


@bp.route("/<int:category_id>")
def category(category_id):
    page = request.args.get("page", 1, type=int)
    category = Category.query.get_or_404(category_id)
    categories = Category.query.all()
    products = category.products.filter(Product.quantity != 0).paginate(
        page=page, per_page=15
    )
    return render_template(
        "category.html", categories=categories, category=category, products=products
    )

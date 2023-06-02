from flask import Blueprint, request, render_template, redirect, flash, url_for
from app.models import Product

bp = Blueprint("product", __name__)


@bp.route("/")
def index():
    reference = request.args.get("reference")
    if reference:
        product = Product.query.filter(Product.reference.like(f"%{reference}%")).first()
        if product:
            return redirect(url_for("product.product", product_id=product.id))

    flash("No se ha encontrado un producto")
    return redirect(url_for("category.index"))


@bp.route("/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product.html", product=product)

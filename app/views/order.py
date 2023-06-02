import uuid
from flask import (
    Blueprint,
    g,
    session,
    request,
    render_template,
    redirect,
    abort,
    url_for,
    flash,
)
from app.extensions import db
from app.models import Order, OrderEntry
from app.utils import or_400

bp = Blueprint("order", __name__)


@bp.before_request
def before_request():
    g.user_id = session.get("user_id")
    if g.user_id is None:
        g.user_id = str(uuid.uuid4())
        session["user_id"] = g.user_id


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        orders = Order.query.filter(Order.user_id == g.user_id)
        return render_template("order.html", orders=orders)
    elif or_400(request.form.get("_method")) == "POST":
        try:
            order = Order(
                user_id=g.user_id,
                name=or_400(request.form.get("name")),
                person_id=or_400(request.form.get("personId")),
                address=or_400(request.form.get("address")),
                city=or_400(request.form.get("city")),
                phone=or_400(request.form.get("phone")),
                email=or_400(request.form.get("email")),
            )
            db.session.add(order)
            db.session.commit()
            return redirect(url_for("order.index"))
        except:
            db.session.rollback()
            raise
    elif or_400(request.form.get("_method")) == "DELETE":
        try:
            order = or_400(
                Order.query.filter(
                    Order.id == request.form.get("id", type=int, default=-1),
                    Order.user_id == g.user_id,
                ).first()
            )
            db.session.delete(order)
            db.session.commit()
            return redirect(url_for("order.index"))
        except:
            db.session.rollback()
            raise
    else:
        abort(400)


@bp.route("/<int:order_id>", methods=["GET", "POST"])
@bp.route("/<order_selector>", methods=["GET", "POST"])
def order(order_id=None, order_selector=None):
    if order_id is None:
        if order_selector == "active" and "active" in session:
            order_id = session["active"]
        else:
            flash("No hay una orden activa")
            return redirect(url_for("order.index")), 404
    if request.method == "GET":
        orders = Order.query.filter(Order.user_id == g.user_id)
        order = Order.query.filter(
            Order.id == order_id, Order.user_id == g.user_id
        ).first_or_404()

        session["active"] = order.id
        return render_template("order.html", orders=orders, order=order)
    elif or_400(request.form.get("_method")) == "POST":
        try:
            order_id = (
                Order.query.filter(Order.id == order_id, Order.user_id == g.user_id)
                .first_or_404()
                .id
            )
            order_entry = OrderEntry(
                quantity=request.form.get("quantity", type=int, default=0),
                price=request.form.get("price", type=float, default=0),
                specification_id=request.form.get("specification", type=int, default=0),
                order_id=order_id,
            )
            db.session.add(order_entry)
            db.session.commit()
            return redirect(url_for("order.order", order_id=order_id))
        except:
            db.session.rollback()
            raise
    elif or_400(request.form.get("_method")) == "DELETE":
        try:
            order_id = (
                Order.query.filter(Order.id == order_id, Order.user_id == g.user_id)
                .first_or_404()
                .id
            )
            order_entry = or_400(
                OrderEntry.query.filter(
                    OrderEntry.id == request.form.get("id", type=int, default=-1),
                    Order.id == order_id,
                ).first()
            )
            db.session.delete(order_entry)
            db.session.commit()
            return redirect(url_for("order.order", order_id=order_id))
        except:
            db.session.rollback()
            raise
    elif or_400(request.form.get("_method")) == "PUT":
        try:
            order_id = (
                Order.query.filter(Order.id == order_id, Order.user_id == g.user_id)
                .first_or_404()
                .id
            )
            order_entry = or_400(
                OrderEntry.query.filter(
                    OrderEntry.id == request.form.get("id", type=int, default=-1),
                    Order.id == order_id,
                ).first()
            )
            order_entry.price = request.form.get(
                "price", type=float, default=order_entry.price
            )
            order_entry.quantity = request.form.get(
                "quantity", type=int, default=order_entry.quantity
            )
            db.session.commit()
            return redirect(url_for("order.order", order_id=order_id))
        except:
            db.session.rollback()
            raise
    else:
        abort(400)

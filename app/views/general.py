from flask import (
    Blueprint,
    g,
    current_app,
    request,
    session,
    render_template,
    redirect,
    url_for,
    flash,
)

bp = Blueprint("general", __name__)


@bp.before_app_request
def before_request():
    session.permanent = True
    g.is_admin = session.get("is_admin", default=False)


@bp.route("/")
def index():
    return redirect(url_for("order.index"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (
            request.form["username"] == current_app.config["ADMIN_USERNAME"]
            and request.form["password"] == current_app.config["ADMIN_PASSWORD"]
        ):
            session["is_admin"] = True
            flash("Se ha iniciado sesión")
            return redirect(url_for("general.index"))
        else:
            flash("Nombre de usuario o contraseña incorrectos")

    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    session["is_admin"] = False
    return redirect(url_for("general.index"))

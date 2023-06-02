from flask import Flask
from config import Config
from app.extensions import db
from app.admin import admin


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensions
    db.init_app(app)
    admin.init_app(app)

    # Blueprints
    from app.views.image import bp as image_bp
    from app.views.product import bp as product_bp
    from app.views.category import bp as category_bp
    from app.views.order import bp as order_bp
    from app.views.general import bp as general_bp

    app.register_blueprint(image_bp, url_prefix="/images")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(category_bp, url_prefix="/categories")
    app.register_blueprint(order_bp, url_prefix="/orders")
    app.register_blueprint(general_bp)
    return app

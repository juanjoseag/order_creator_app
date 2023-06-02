from flask import Markup, request, session, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_wtf.file import FileField
from app.extensions import db
from app.models import Category, Product, Specification, Image


class AdminModelView(ModelView):
    def is_accessible(self):
        return session.get("is_admin", default=False)


class CategoryView(AdminModelView):
    def _list_products(view, context, model, name):
        return Markup(
            f"<ul>{''.join(f'<li>{product.reference}</li>' for product in model.products if product)}</ul>"
        )

    column_hide_backrefs = False
    column_searchable_list = ["name"]
    column_list = ("name", "products")
    column_labels = {"name": "Nombre", "products": "Productos"}
    column_formatters = {"products": _list_products}


class ProductView(AdminModelView):
    def _list_specifications(view, context, model, name):
        return Markup(
            f"<ul>{''.join(f'<li>{specification.size} - {specification.color} <b>({specification.quantity})</b></li>' for specification in model.specifications if specification)}"
        )

    def _list_images(view, context, model, name):
        return Markup(
            f"<ul>{''.join(f'<li>{image.id}</li>' for image in model.images if image)}</ul>"
        )

    column_hide_backrefs = False
    column_searchable_list = ["reference", "description"]
    column_list = (
        "reference",
        "description",
        "retail_price",
        "wholesale_price",
        "specifications",
        "images",
    )
    column_labels = {
        "reference": "Referencia",
        "description": "Descripcción",
        "retail_price": "Precio al por menor",
        "wholesale_price": "Precio al por mayor",
        "specifications": "Especificaciones",
        "images": "Imágenes",
    }
    column_formatters = {"specifications": _list_specifications, "images": _list_images}


class SpecificationView(AdminModelView):
    def _list_product(view, context, model, name):
        return model.product.reference

    column_hide_backrefs = False
    column_searchable_list = ["product.reference"]
    column_list = ("size", "color", "quantity", "product")
    column_labels = {
        "size": "Tamaño",
        "color": "Color",
        "quantity": "Cantidad",
        "product": "Producto",
    }
    column_formatters = {
        "product": _list_product,
    }


class ImageView(AdminModelView):
    def on_model_change(self, form, model, is_created):
        image_file = request.files["image"]
        if image_file is not None:
            model.image = image_file.read()
            model.mimetype = image_file.mimetype

    def _list_image(view, context, model, name):
        if not model.image or not model.mimetype:
            return ""
        return Markup(
            f'<img src="{url_for("image.image", image_id=model.id)}" style="max-width: 300px">'
        )

    form_extra_fields = {"image": FileField("Image")}

    column_searchable_list = ["id", "product.reference"]
    column_list = ("id", "image", "mimetype", "main")
    column_labels = {"image": "Imagen", "main": "Principal"}
    column_formatters = {"image": _list_image}


admin = Admin(template_mode="bootstrap4", index_view=AdminIndexView(name="Inicio"))
admin.add_view(
    CategoryView(Category, db.session, endpoint="admin_category", name="Categorías")
)
admin.add_view(
    ProductView(Product, db.session, endpoint="admin_product", name="Productos")
)
admin.add_view(
    SpecificationView(
        Specification,
        db.session,
        endpoint="admin_specification",
        name="Especificaciones",
    )
)
admin.add_view(ImageView(Image, db.session, endpoint="admin_image", name="Imágenes"))

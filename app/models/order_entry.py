from app.extensions import db
from app.models.product import Product
from app.models.specification import Specification
from app.utils import EmptyObject


class OrderEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    specification_id = db.Column(db.Integer, db.ForeignKey("specification.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))

    def __repr__(self):
        return f"<OrderEntry '{self.id}'>"

    @property
    def specfication(self, default=EmptyObject()):
        specification = Specification.query.get(self.specification_id)
        if specification is not None:
            return specification
        else:
            return default

    @property
    def product(self, default=EmptyObject()):
        specification = Specification.query.get(self.specification_id)
        if specification is not None:
            return Product.query.get(specification.product_id)
        else:
            return default

    @property
    def image(self, default=EmptyObject()):
        specification = Specification.query.get(self.specification_id)
        if specification is not None:
            return Product.query.get(specification.product_id).main_images.first()
        else:
            return default

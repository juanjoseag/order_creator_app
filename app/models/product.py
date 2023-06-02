from app.extensions import db
from app.models.image import Image


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.Text, unique=True)
    description = db.Column(db.Text)
    retail_price = db.Column(db.Float)
    wholesale_price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    specifications = db.relationship("Specification", backref="product", lazy="dynamic")
    images = db.relationship("Image", backref="product", lazy="dynamic")

    def __repr__(self):
        return f"<Product '{self.reference}'>"

    @property
    def quantity(self):
        count = 0
        for specification in self.specifications:
            if specification.quantity < 0:
                return -1
            else:
                count += specification.quantity
        return count

    @property
    def main_images(self):
        return self.images.filter(Image.main == True)

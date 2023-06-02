from app.extensions import db


class Specification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Text)
    color = db.Column(db.Text)
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    order_entries = db.relationship(
        "OrderEntry", backref="specification", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Specification '{self.size}' - '{self.color}'>"

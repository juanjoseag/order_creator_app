from app.extensions import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    products = db.relationship("Product", backref="category", lazy="dynamic")

    def __repr__(self):
        return f"<Category '{self.name}'>"

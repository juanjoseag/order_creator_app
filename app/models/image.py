from app.extensions import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary)
    mimetype = db.Column(db.Text)
    main = db.Column(db.Boolean, default=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))

    def __repr__(self):
        return f"<Image '{self.id}'>"

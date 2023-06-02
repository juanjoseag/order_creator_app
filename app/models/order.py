from app.extensions import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text)
    name = db.Column(db.Text)
    person_id = db.Column(db.Text)
    address = db.Column(db.Text)
    city = db.Column(db.Text)
    phone = db.Column(db.Text)
    email = db.Column(db.Text)
    order_entries = db.relationship("OrderEntry", backref="order", lazy="dynamic")

    def __repr__(self):
        return f"<Order '{self.name}'>"

    @property
    def total(self):
        count = 0
        for entry in self.order_entries:
            count += entry.quantity * entry.price
        return count

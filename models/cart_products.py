from db import db
from sqlalchemy.dialects.mysql import BIGINT

# item, order, quantity


class Class_products(db.Model):
    id = db.Column(BIGINT(unsigned=True), primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(BIGINT(unsigned=True),
                           db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer)

    def __init__(self, cart_id, product_id, quantity):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity

    @classmethod
    def add_product(cls, cart_id, product_id, quantity):
        cart_product = Class_products.query.filter_by(
            cart_id=cart_id, product_id=product_id).first()

        if not cart_product:
            cart_product = Class_products(cart_id, product_id, quantity)
            db.session.add(cart_product)
            db.session.commit()

        else:
            cart_product.product_id = quantity

    @classmethod
    def remove_from_cart(cls, cart_id, product_id):
        print("cart id: ", cart_id)
        print("product_id", product_id)
        product = Class_products.query.filter_by(
            cart_id=cart_id, product_id=product_id).first()
        print("-------->PRODUCT: ", end='')
        print(product)

        if product is not None:
            db.session.delete(product)
            db.session.commit()

from db import db
from sqlalchemy.dialects.mysql import BIGINT
from .messenger_user import MessengerUser
from .cart_products import Class_products


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(BIGINT(unsigned=True),
                        db.ForeignKey('messenger_user.id'))

    # 0 means not ordered, 1 means already ordered
    ordered = db.Column(db.Boolean, default=0)

    # products is for association

    # TODO: give other fields here

    def __init__(self, user_id):
        self.user_id = user_id

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_cart(cls, messenger_user_id):
        user_id = MessengerUser.get_id(messenger_user_id)
        # it is checking if the cart has been ordered or not
        cart = Cart.query.filter_by(user_id=user_id, ordered=0).first()

        if not cart:
            cart=Cart(user_id)
            return cart
        else:
            return cart

    def add_product(self, product_id, quantity):
        Class_products.add_product(self.id, product_id, quantity)

    def remove_product(self, product_id):
        Class_products.remove_from_cart(self.id, product_id)

    def get_products(self):
        cart_products = Class_products.query.filter_by(cart_id=self.id).all()
        return cart_products

from db import db
from .carts import Cart
from .cart_products import Class_products
from .products import Product


class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))

    # add status here

    def __init__(self, messenger_user_id):

        cart = Cart.get_cart(messenger_user_id)
        cart.ordered = 1
        self.cart_id = cart.id

        db.session.add(cart)
        db.session.add(self)

        db.session.commit()

    # TODO: get location from graph api

    @classmethod
    def get_receipt(cls, messenger_user_id):
        """needs refactoring, need to create association in the models, using the association objects"""
        """or a single query will suffice"""
        order=cls(messenger_user_id)

        print("Order: ",order.cart_id)

        products_relation = Class_products.query.filter_by(
            cart_id=order.cart_id).all()

        product_ids = []
        product_quantites = []
        product_img_urls = []

        for product in products_relation:
            product_ids.append(product.product_id)
            product_quantites.append(product.quantity)

        total_price = 0
        # calculate quantity here

        product_names = []
        product_prices = []

        for product_id, product_quantity in zip(product_ids, product_quantites):
            # price=Product.query.get(product_id).price*product_quantity

            prod = Product.query.get(product_id)
            product_names.append(prod.name)
            product_prices.append(prod.price)
            product_img_urls.append(prod.img_url)
            price=prod.price * product_quantity


            print("price in the loop", price)  # FIXME: remove in production
            print("quantity in the loop", product_quantity)
            print("name in the loop", prod.name)
            print("price in the loop", prod.price)
            total_price += price

            # recipt can be shown from here
        return product_names,product_prices, product_quantites, product_img_urls, total_price, order.id #we can return all the lists from here

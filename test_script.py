from models.categories import Category
from models.products import Product
from models.carts import Cart
from models.messenger_user import MessengerUser


print(MessengerUser.get_id(3127097767305306))
cart=Cart.get_cart(3127097767305306)
cart.add_product(1,2)
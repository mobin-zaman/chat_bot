from flask import Flask, request
from pprint import pprint
from fbmq import Page, Template, QuickReply
from flask_migrate import Migrate
from db import db
import sys
import time  # FIXME: report it in the production
from collections import defaultdict
# TODO: add redis layer
""" M O D E L S """
from models.categories import Category
from models.products import Product
from models.messenger_user import MessengerUser
from models.carts import Cart
"""EOF"""


"""     C O N S T A N T S  """
PAGE_ACCESS_TOKEN = "EAAkxYspVIqgBANJbHTxnhLPX4SPWcHvJtolWFmyeZBhOI1vO6G4BAghOXJyH6ZCuUiCKs9vdmjD3xy3Gz5GfTqIxIdjxPW2TUUWNWnRNBQvl2cjSr1G1qv8k9QP8WmmvSELSUSKcWGfsyPIIQ4RDtFTpR5Jc6ZCII3Y7NUfdAZDZD"
VERIFY_TOKEN = "this is the veryfy token"
"""     End Of Constants    """

"""app instance setup"""
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://username:password@localhost/bot_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "horhe borhes"
""" EOF """

""" Flask_Migrate instance """
migrate = Migrate(app, db)

""" page instance setup """
page = Page(PAGE_ACCESS_TOKEN)
page.show_starting_button("GET_STARTED")
page.show_persistent_menu([Template.ButtonPostBack('contact info', 'PERSISTENT_CONTACT_INFO'),
                           Template.ButtonWeb("MOVEONCOMPANY", "www.google.com")])
page.greeting("Hello!")
""" EOF """
"""for modularity"""
""" EOF """


@app.route('/', methods=['POST'])
def webhook():
    """the center of all """
    data = request.get_json()
    # pprint(data)  #FIXME: remove this line from production
    page.handle_webhook(request.get_data(as_text=True))
    return "ok", 200


@app.route('/', methods=['GET'])
def receive_message():
    token_sent = request.args.get("hub.verify_token")
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid Request"


@page.handle_message
def message_handler(event):
    sender_id = event.sender_id
    message = event.message.get('text')
    print(message)


"""LIST OF QUICK REPLIES"""
starter = [
    # explore means showing categories
    QuickReply(title="explore!", payload='SHOW_CATEGORIES'),
    # show the location on a zone basis
    QuickReply(title="get locations", payload='SHOW_INFO')
]


"""EOF"""


@page.callback(['GET_STARTED'])
def get_started(payload, event):
    """get started callback"""
    sender_id = event.sender_id

    # now initiate a messenger_user
    MessengerUser(sender_id)
    print("+++----INITIATED USER-------+++")

    # FIXME: use graph api to get username

    page.send(sender_id, message="hello user")
    page.send(sender_id, "options for you", quick_replies=starter)


def template_categories():
    categories = Category.query.all()
    templates = []
    print("is it working?")
    for category in categories:
        # FIXME: regex needs to be checked on double digit
        payload = "SHOW_PRODUCTS|" + str(category.id)
        print("PAYLOAAAAD: ", payload)
        single_template = Template.GenericElement(category.name,
                                                  subtitle=category.description,
                                                  image_url=category.img_url,
                                                  buttons=[
                                                      Template.ButtonPostBack(
                                                          "show products", payload)
                                                  ])
        templates.append(single_template)

    return templates


def template_products(category_id):
    category = Category.query.get(category_id)
    products = category.products

    templates = []
    for product in products:
        single_template = Template.GenericElement(product.name, subtitle=str(product.price), image_url=product.img_url,
                                                  buttons=[Template.ButtonPostBack("View Description",
                                                                                   payload="PRODUCT_DESCRIPTION|" + str(
                                                                                       product.id)),
                                                           Template.ButtonPostBack("Add To Cart",
                                                                                   payload="ADD_TO_CART|" + str(
                                                                                       product.id))])
        templates.append(single_template)

    # below one is different from products`
    return templates  # TODO: TRUE OF FALSE for square image, need to check what that is


@page.callback(['SHOW_PRODUCTS|0'])
def show_products(payload, event):
    selected_id = payload.split('|')[1]
    print("------------CATEGORY_ID: ", selected_id)

    navigation = [
        QuickReply("explore categories", payload="SHOW_CATEGORIES"),
        QuickReply("check cart", payload="CHECK_CART")
    ]

    templates = template_products(selected_id)

    template_dict = defaultdict(list)
    count = 0
    dict_count = 0  # FIXME: add comments here
    for template in templates:
        template_dict[dict_count].append(template)
        count += 1
        if count == 10:
            dict_count += 1
            count = 0

    for temp_dict in template_dict.values():
        pprint(temp_dict)
        page.send(event.sender_id, Template.Generic(temp_dict, True))

    page.send(event.sender_id, "or explore categories",
              quick_replies=navigation)


@page.callback(['SHOW_CATEGORIES'])
def show_categories(payload, event):
    """function to show categories"""

    print("show_categories()")
    page.send(event.sender_id, "showing categories")
    templates = template_categories()
    template_dict = defaultdict(list)
    count = 0
    dict_count = 0
    for template in templates:
        template_dict[dict_count].append(template)
        count += 1
        if count == 10:
            dict_count += 1
            count = 0

    for temp_dict in template_dict.values():
        pprint(temp_dict)
        page.send(event.sender_id, Template.Generic(temp_dict, True))


@page.callback(['PRODUCT_DESCRIPTION|0'])
def show_product_description(payload, event):
    selected_id = payload.split('|')[1]
    print("__________PROCUT_ID: ", selected_id)

    category_id = str(Product.get_category_id(selected_id))

    navigation = [
        QuickReply("products", payload="SHOW_PRODUCTS|" + category_id),
        QuickReply("categories", payload="SHOW_CATEGORIES")
    ]

    page.send(event.sender_id, Product.get_description(selected_id))
    page.send(event.sender_id, "Continue navigatation",
              quick_replies=navigation)
    # TODO: add UX here


@page.callback(['ADD_TO_CART|0'])
def select_to_cart(payload, event):
    selected_product_id = payload.split('|')[1]
    print("______CART_SELECTED_ID", selected_product_id)

    navigation = [
        QuickReply("1", payload="QUANTITY|1|" + str(selected_product_id)),
        QuickReply("2", payload="QUANTITY|2|" + str(selected_product_id)),
        QuickReply("3", payload="QUANTITY|3|" + str(selected_product_id)),
        QuickReply("4", payload="QUANTITY|4|" + str(selected_product_id)),
        QuickReply("5", payload="QUANTITY|5|" + str(selected_product_id)),
    ]

    page.send(event.sender_id, "Select quantity: ", quick_replies=navigation)


@page.callback(['QUANTITY|0|0'])
def add_to_cart(payload, event):
    none, quantity, product_id = payload.split('|')
    print("-------PRODUCT ID, QUANTITY____:", product_id, quantity)

    cart = Cart.get_cart(event.sender_id)
    cart.add_product(product_id, quantity)

    print("Exception happening here I think")

    navigation = [
        QuickReply("categories", payload="SHOW_CATEGORIES"),
        QuickReply("check cart", payload="CHECK_CART")
    ]

    page.send(event.sender_id, "added to cart", quick_replies=navigation)


def template_cart_products(sender_id):
    cart = Cart.get_cart(sender_id)
    products = cart.get_products()
    pprint(products)
    templates = []
    if len(products) == 0:
        navigation = [
            QuickReply("explore categories", "SHOW_CATEGORIES")
        ]
        print("template_cart_products()")
        page.send(sender_id, "your cart is empty, continue exploring",quick_replies=navigation)

    else:
        for product in products:
            print(product.product_id)
            print(product.quantity)

            #refactor it :'(
            product_ = Product.query.filter_by(id=product.product_id).first()
            payload = "REMOVE_FROM_CART|"+str(product.product_id)
            print("========>", payload)
            template = Template.GenericElement(product_.name, subtitle=str(product_.price) + "৳ (x" + str(
                product.quantity) + ")", image_url=product_.img_url,
                buttons=[Template.ButtonPostBack("remove from cart", payload), Template.ButtonPostBack("CHECKOUT!", "CHECKOUT")])
            templates.append(template)

        page.send(sender_id, Template.Generic(templates))


@page.callback(["CHECKOUT"])
def check_out(payload, event):
    print("CHECKOUT COMPLETED")
    pass


@page.callback(["CHECK_CART"])
def check_cart(payload, event):
    template_cart_products(event.sender_id)


@page.callback(["REMOVE_FROM_CART|0"])
def remove_from_cart(payload, event):
    cart = Cart.get_cart(event.sender_id)

    product_id = payload.split('|')[1]
    print("========> PRODUCT_ID: ",product_id)
    cart.remove_product(product_id)

    navigation = [
        QuickReply("explore categories", payload="SHOW_CATEGORIES"),
        QuickReply("check cart", payload="CHECK_CART"),
    ]

    page.send(event.sender_id, "product removed", quick_replies=navigation)


@page.callback(['SHOW_INFO'])
def show_informations(payload, event):
    page.send(event.sender_id, "this is a sample information")
    page.send(event.sender_id, "okay fine", quick_replies=starter)


# @page.handle_message
# def message_handler(event):
#     """:type event: fbmq.Event"""
#     sender_id = event.sender_id
#     message = event.message_text

#     page.send(sender_id, "thank you! your message is '%s'" % message)


# @page.after_send
# def after_send(payload, response):
#     """:type payload: fbmq.Payload"""
#     print("complete")

# app.app_context().push()
if __name__ == "__main__":
    db.init_app(app)

    # import test_script

    app.run(debug=True)

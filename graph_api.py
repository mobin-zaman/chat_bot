import requests
from app import PAGE_ACCESS_TOKEN
from pprint import pprint  # FIXME: remove this line from prodution


def user_info_json(sender_id):  # this will be replaced by get user profile
    """retrieves the json from graph api, which is used for other helper functions"""

    """whatever data needed should be added in the below API_URL"""
    API_URL = "https://graph.facebook.com/{}?fields=first_name,last_name&access_token={}".format(
        sender_id, PAGE_ACCESS_TOKEN)
    response = requests.get(API_URL)
    return response.json()


def get_first_name(sender_id):
    """retrives the first name from the json of user_info_json"""
    data = user_info_json(sender_id)
    return data['first_name']


def get_last_name(sender_id):
    """retrives the last name from the json"""
    data = user_info_json(sender_id)
    return data['last_name']


# TODO: how to get basic location and phone number data?
# TODO : should graph api should be used or the page functionality?
 
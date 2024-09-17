import configparser
# import logging

import requests.exceptions
from blizzardapi2 import BlizzardApi

# Lets get this logging shit out of the way for now
# logger = logging.getLogger('wowapi')
# logger.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

config = configparser.ConfigParser()
config.read('config.ini')

# logger.info('Game Data API Example')

api_client = BlizzardApi(config.get('CLIENT', 'ClientID'), config.get('CLIENT', 'ClientSecret'))


# TODO build a search function using the search endpoint (in the config file). This will need to get an access token
#  from the OAuth server and pass it as a parameter to the HTTP request that returns the itemID
#
# def search_For_Item(name):
#  result = some OAuth fuckery here.

def get_item_from_api(item_id):
    item = ""
    try:
        item = api_client.wow.game_data.get_item('eu', "en_GB", item_id)
    except requests.exceptions.HTTPError:
        pass
    if item:
        return format_item(item)


def format_item(item):
    return_string = ''
    stats_list = ''
    spell_list = ''
    item_id = ''
    try:
        item_id = item['preview_item']['item']['id']
    except Exception:
        pass
    try:
        name = item['preview_item']['name']
        return_string = return_string + f"{name}\n"
    except Exception:
        pass
    try:
        quality = item['preview_item']['quality']['name']
        return_string = return_string + f"{quality}\n"
    except Exception:
        pass
    # TODO - Some items have class requirements that appear in this bit as an element of a dictionary. Must iterate
    #  over and pull that information out. Check out Glyphs.
    #
    try:
        required_level = item['preview_item']['requirements']['level']['display_string']
        return_string = return_string + f"{required_level}\n"
    except Exception:
        pass
    try:
        item_level = item['preview_item']['level']['display_string']
        return_string = return_string + f"{item_level}\n"
    except Exception:
        pass
    try:
        bind = item['preview_item']['binding']['name']
        return_string = return_string + f"{bind}\n"
    except Exception:
        pass
    try:
        limit_category = item['preview_item']['limit_category']
        return_string = return_string + f"{limit_category}\n"
    except Exception:
        pass
    bag_slots = ""
    try:
        bag_slots = item['preview_item']['container_slots']['display_string']
        return_string = return_string + f"{bag_slots}\n"
    except Exception:
        pass
    try:
        if not bag_slots:
            inventory_type = item['preview_item']['inventory_type']['name']
            return_string = return_string + f"{inventory_type}\n"
    except Exception:
        pass
    try:
        for count in range(len(item['preview_item']['stats'])):
            stats_list = stats_list + f"{item['preview_item']['stats'][count]['display']['display_string']}\n"
        stats_list = stats_list.rstrip()
        return_string = return_string + f"{stats_list}\n"
    except Exception:
        pass

    try:
        for count in range(len(item['preview_item']['spells'])):
            spell_list = spell_list + f"{item['preview_item']['spells'][count]['description']}\n"
        spell_list = spell_list.rstrip()
        return_string = return_string + f"{spell_list}\n"
    except Exception:
        pass

    try:
        requirement = f"{item['preview_item']['requirements']['skill']['display_string']}"
        return_string = return_string + f"{requirement}\n"
    except Exception:
        pass
    try:
        description = f"{item['preview_item']['description']}"
        return_string = return_string + f"{description}\n"
    except Exception:
        pass

    try:
        price = (f"{item['preview_item']['sell_price']['display_strings']['header']}" 
                 f"{item['preview_item']['sell_price']['display_strings']['gold']}G "
                 f"{item['preview_item']['sell_price']['display_strings']['silver']}S "
                 f"{item['preview_item']['sell_price']['display_strings']['copper']}C")
        return_string = return_string + f"{price}\n"
    except Exception:
        pass
    return_string = return_string + f"https://www.wowhead.com/item={item_id}"
    if return_string:
        return_string = return_string.rstrip()
    return return_string


# TODO Reagents barely fucking work. Gotta get them sorted out.
# Recipies too.
# And Gems
# Maybe switch based on item type, and have a custom parser for each one?

result = get_item_from_api(212454)
if result:
    print(result)

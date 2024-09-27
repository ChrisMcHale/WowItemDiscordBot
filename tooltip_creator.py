import shutil

from html2image import Html2Image

hti = Html2Image()

with open('css/wowitem.css', 'r') as file:
    css_str = file.read()

with open('html/header.html', 'r') as file:
    html_header = file.read()

with open('html/footer.html', 'r') as file:
    html_footer = file.read()


def __create_item_dictionary(item_JSON):
    item_dictionary = {}
    stats_list = ""
    spell_list = ""
    try:
        item_dictionary.update({"item_id": item_JSON['item']['id']})
    except Exception:
        pass

    # Get the item name
    try:
        item_dictionary.update({"item_name": item_JSON['name']})
    except Exception:
        pass
    try:
        item_dictionary.update({"item_quality": item_JSON['quality']['name']})
    except Exception:
        pass
    # TODO - Some items have class requirements that appear in this bit as an element of a dictionary. Must iterate
    #  over and pull that information out. Check out Glyphs.
    #
    try:
        item_dictionary.update({"required_level": item_JSON['requirements']['level']['display_string']})
    except Exception:
        pass
    try:
        item_dictionary.update({"item_level": item_JSON['level']['display_string']})
    except Exception:
        pass
    try:
        item_dictionary.update({"bind": item_JSON['binding']['name']})
    except Exception:
        pass
    try:
        item_dictionary.update({"limit_category": item_JSON['limit_category']})
    except Exception:
        pass
    bag_slots = ""
    try:
        item_dictionary.update({"bag_slots": item_JSON['container_slots']['display_string']})
    except Exception:
        pass
    try:
        if not bag_slots:
            item_dictionary.update({"inventory_type": item_JSON['inventory_type']['name']})
    except Exception:
        pass
    try:
        for stat in item_JSON['stats']:
            stats_list = stats_list + f"{stat['display']['display_string']}\n"
        item_dictionary.update({"stats_list": stats_list.rstrip()})

    except Exception:
        pass

    try:
        for spell in item_JSON['spells']:
            spell_list = spell_list + f"{spell['description']}\n"
        item_dictionary.update({"spell_list": spell_list.rstrip()})
    except Exception:
        pass

    try:
        item_dictionary.update({"requirement": f"{item_JSON['requirements']['skill']['display_string']}"})
    except Exception:
        pass
    try:
        item_dictionary.update({"description": f"{item_JSON['description']}"})
    except Exception:
        pass

    try:
        item_dictionary.update({"price": f"{item_JSON['sell_price']['display_strings']['header']}"})
        item_dictionary.update({"price-gold": f"{item_JSON['sell_price']['display_strings']['gold']}"})
        item_dictionary.update({"price-silver": f"{item_JSON['sell_price']['display_strings']['silver']}"})
        item_dictionary.update({"price-copper": f"{item_JSON['sell_price']['display_strings']['copper']}"})



    except Exception:
        pass
    print(item_dictionary)
    html_body = '<div class="tooltip">\n'
    # Get the ID of the item, we'll need this to save the file.
    html_body = html_body + f"<div class='item-name {str(item_dictionary.get("item_quality")).lower()}'>{str(item_dictionary.get("item_name"))}</div>\n"
    html_body = html_body + f"<div class='item-level'>{str(item_dictionary.get("item_level"))}</div>\n"
    html_body = html_body + f"<div class='item-binding'>{str(item_dictionary.get("bind"))}</div>\n"
    html_body = html_body + f"<div class='item-stats'>\n"
    html_body = html_body + f"<div class='stat'>{str(item_dictionary.get("stats_list"))}</div>\n"
    html_body = html_body + f"<div class='item-effect'>{str(item_dictionary.get("spell_list"))}</div>\n"
    html_body = html_body + f"<div class='item-requirement'>{str(item_dictionary.get("required_level"))}</div>\n"
    html_body = html_body + f"<div class='sellprice'>{str(item_dictionary.get("price"))} {str(item_dictionary.get("price-gold"))}<img src=\"https://wow.zamimg.com/images/icons/money-gold.gif\" alt=\"Gold\"> {str(item_dictionary.get("price-silver"))}<img src=\"https://wow.zamimg.com/images/icons/money-silver.gif\" alt=\"Silver\">  {str(item_dictionary.get("price-copper"))}<img src=\"https://wow.zamimg.com/images/icons/money-copper.gif\" alt=\"Copper\">  </div>\n"
    html_body = html_body + f"</div>\n"
    html_str = html_header + html_body + html_footer
    print(html_str)
    print(f"printing name {str(item_dictionary.get("item_name"))}")

    hti.screenshot(html_str=html_str, css_str=css_str, save_as=f'{item_dictionary.get("item_id")}.png')
    shutil.move(f'{item_dictionary.get("item_id")}.png', f'./tooltips/{item_dictionary.get("item_id")}.png')
    return f'{item_dictionary.get("item_id")}.png'


def create_tooltip(search_term):
    file_path = __create_item_dictionary(search_term)
    return file_path

#
# def create_tooltip(search_term):
#
#     __create_tooltip_from_JSON(item_JSON)
#     return None

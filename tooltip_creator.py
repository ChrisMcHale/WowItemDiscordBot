import os
import shutil

from html2image import Html2Image

import image_cropper

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
    # Item ID
    try:
        item_dictionary.update({"item_id": item_JSON['item']['id']})
    except Exception:
        pass

    # Item Name
    try:
        item_dictionary.update({"item_name": item_JSON['name']})
    except Exception:
        pass

    # Item Quality
    try:
        item_dictionary.update({"item_quality": item_JSON['quality']['name']})
    except Exception:
        pass
    # TODO - Some items have class requirements that appear in this bit as an element of a dictionary. Must iterate
    #  over and pull that information out. Check out Glyphs.
    #

    # Level Requirement
    try:
        item_dictionary.update({"required_level": item_JSON['requirements']['level']['display_string']})
    except Exception:
        pass

    # Item Level
    try:
        item_dictionary.update({"item_level": item_JSON['level']['display_string']})
    except Exception:
        pass

    # Bind Type
    try:
        item_dictionary.update({"bind": item_JSON['binding']['name']})
    except Exception:
        pass

    # Limit Category
    try:
        item_dictionary.update({"limit_category": item_JSON['limit_category']})
    except Exception:
        pass

    # Bag Slots
    bag_slots = ""
    try:
        item_dictionary.update({"bag_slots": item_JSON['container_slots']['display_string']})
    except Exception:
        pass

    # Inventory Type
    try:
        if not bag_slots:
            item_dictionary.update({"inventory_type": item_JSON['inventory_type']['name']})
    except Exception:
        pass

    # Item Stats
    try:
        for stat in item_JSON['stats']:
            stats_list = stats_list + f"{stat['display']['display_string']}</br>"
        item_dictionary.update({"stats_list": stats_list.rstrip()})
    except Exception:
        pass

    # Item Spells
    try:
        for spell in item_JSON['spells']:
            spell_list = spell_list + f"{spell['description']}</br>"
        item_dictionary.update({"spell_list": spell_list.rstrip()})
    except Exception:
        pass

    # Skill Requirement
    try:
        item_dictionary.update({"requirement": f"{item_JSON['requirements']['skill']['display_string']}"})
    except Exception:
        pass

    # Item Description
    try:
        item_dictionary.update({"description": f"{item_JSON['description']}"})
    except Exception:
        pass

    # Cost
    try:
        item_dictionary.update({"price": f"{item_JSON['sell_price']['display_strings']['header']}"})
        item_dictionary.update({"price-gold": f"{item_JSON['sell_price']['display_strings']['gold']}"})
        item_dictionary.update({"price-silver": f"{item_JSON['sell_price']['display_strings']['silver']}"})
        item_dictionary.update({"price-copper": f"{item_JSON['sell_price']['display_strings']['copper']}"})
    except Exception:
        pass

    print(item_dictionary)
    # Here we build up the HTML body tag with the contents of the JSON file.
    # TODO - we should really be checking for nulls on the values, not all items have values for each attribute
    html_body = '<div class="tooltip">\n'
    html_body = html_body + f"<div class='item-name {str(item_dictionary.get("item_quality")).lower()}'>{str(item_dictionary.get("item_name"))}</div>\n"
    html_body = html_body + f"<div class='item-level'>{str(item_dictionary.get("item_level"))}</div>\n"
    html_body = html_body + f"<div class='item-binding'>{str(item_dictionary.get("bind"))}</div>\n"
    html_body = html_body + f"<div class='item-stats'>\n"
    html_body = html_body + f"<div class='stat'>{str(item_dictionary.get("stats_list"))}</div>\n"
    html_body = html_body + f"<div class='item-effect'>{str(item_dictionary.get("spell_list"))}</div>\n"
    html_body = html_body + f"<div class='item-requirement'>{str(item_dictionary.get("required_level"))}</div>\n"
    html_body = html_body + f"<div class='sellprice'>{str(item_dictionary.get("price"))} {str(item_dictionary.get("price-gold"))}<img src=\"https://wow.zamimg.com/images/icons/money-gold.gif\" alt=\"Gold\"> {str(item_dictionary.get("price-silver"))}<img src=\"https://wow.zamimg.com/images/icons/money-silver.gif\" alt=\"Silver\">  {str(item_dictionary.get("price-copper"))}<img src=\"https://wow.zamimg.com/images/icons/money-copper.gif\" alt=\"Copper\">  </div>\n"
    html_body = html_body + f"</div>\n"

    # Add the header and footer to make it a legitimate HTML file
    html_str = html_header + html_body + html_footer
    # use the HTML to Image library to create a PNG, which unforunatley comes out as a 1920x1080 file
    hti.screenshot(html_str=html_str, css_str=css_str, save_as=f'{item_dictionary.get("item_id")}.png')

    # Crop the image down to just the item tooltip
    image_cropper.crop_image(f'{item_dictionary.get("item_id")}.png')

    # Put the tooltip png in the right folder and remove the original
    shutil.move(f'{item_dictionary.get("item_id")}_cropped.png', f'./tooltips/{item_dictionary.get("item_id")}.png')
    os.remove(f'{item_dictionary.get("item_id")}.png')

    # Pass back the name of the tooltip picture
    return f'{item_dictionary.get("item_id")}.png'


def create_tooltip(item_JSON):
    file_path = __create_item_dictionary(item_JSON)
    return file_path

#
# def create_tooltip(search_term):
#
#     __create_tooltip_from_JSON(item_JSON)
#     return None

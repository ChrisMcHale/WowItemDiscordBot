# import bot
from api import wowapihelper
import logging
import configparser

logger = logging.getLogger('wowapi')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
# bot = bot
api = wowapihelper
config = configparser.ConfigParser()
config.read('config.ini')
# TODO like.. everyting?
def initialise_bot():
    logger.info("Bot Started")
    print(api.search_for_item('S'))
    pass


if __name__ == '__main__':
    initialise_bot()
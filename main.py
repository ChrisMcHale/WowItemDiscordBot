# bot.py - The Entry Point
import configparser
import datetime
import logging
import re

import discord

import tooltip_creator
import wowapihelper

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
logging.basicConfig(filename='wowbot.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s - %(message)s')

# Load in the Environmental Variables from the local .env file
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get('BOT', 'TOKEN')
GUILD_NAME = config.get('BOT', 'GUILD_NAME')
# DB_USER = os.getenv('DATABASE_USER')
# DB_PASSWORD = os.getenv('DATABASE_PASSWORD')
# DB_HOST = os.getenv('DATABASE_HOST')
# DB_SCHEMA = os.getenv('DATABASE_SCHEMA')
BOT_PREFIX = config.get('BOT', 'BOT_PREFIX')
HELP_MESSAGE = config.get('BOT', 'HELP_MESSAGE')


# Local string formatted date method
def get_current_datetime():
    current_date_time = datetime.datetime.now()
    return current_date_time.strftime("%A %d %B %Y %X")


# Set up the Database Connection
# def connect_to_database():
#     config = {
#         "user": DB_USER,
#         "password": DB_PASSWORD,
#         "host": DB_HOST,
#         "database": DB_SCHEMA
#     }
#     try:
#         db_connection = mysql.connector.connect(**config)
#         return db_connection
#     except:
#         print("Connection to DB Failed")
#         exit(1)
#
#
# # Returns the number of times a user said Nice based on their User ID
# def get_nice_count_for_user_id(id):
#     db_connection = connect_to_database()
#     db_cursor = db_connection.cursor()
#     db_cursor.execute(f'SELECT * from nicecount where user_id = {id}')
#     db_result = db_cursor.fetchone()
#     return db_result
#
#
# # Returns the last message from a user based on their User ID
# def get_last_nice_message_for_user_id(id):
#     db_connection = connect_to_database()
#     db_cursor = db_connection.cursor()
#     db_cursor.execute(f'SELECT last_message, latest_nice from nicecount where user_id = {id}')
#     db_result = db_cursor.fetchone()
#     return db_result
#
#
# # Creates a new database entry for a user
# def create_new_nicecount_record(message):
#     db_connection = connect_to_database()
#     db_cursor = db_connection.cursor()
#     sql = "INSERT INTO nicecount (display_name, count, latest_nice, last_message, user_id) values (%s,%s," \
#           "%s,%s,%s) "
#     values = (message.author.name, 1, get_current_datetime(), message.content, message.author.id)
#     db_cursor.execute(sql, values)
#     db_connection.commit()
#
#
# # Updates the user's database entry based on their User ID
# def update_nicecount_record(message):
#     user_nice_count = int(get_nice_count_for_user_id(message.author.id)[2])
#     new_nice_count = str(user_nice_count + 1)
#     db_connection = connect_to_database()
#     db_cursor = db_connection.cursor()
#     sql = f"UPDATE nicecount SET count=%s, latest_nice=%s, last_message=%s WHERE user_id " \
#           f"= {message.author.id} "
#     values = (new_nice_count, get_current_datetime(), message.content)
#     db_cursor.execute(sql, values)
#     db_connection.commit()
#

# Instantiate the Discord Client

client = discord.Client(intents=discord.Intents.all())


# The Client On_Ready event - This fires when the Bot connects to Discord and joins the Guild
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD_NAME)
    log.info(f'{client.user} has connected to Discord and is in the following Guilds:\n'
             f'{guild.name} (id: {guild.id})'
             )
    guild_members = '\n - '.join([member.name for member in guild.members])
    log.info(f'Guild Members:\n - {guild_members}')


def create_embedeed_message(filename):
    file = discord.File(f'./tooltips/{filename}')
    embed = discord.Embed()
    embed.set_image(url="attachment://" + filename)
    return embed, file


@client.event
async def on_message(message):
    if message.guild:
        response = ""
        # Ignore our own messages
        if message.author == client.user:
            return
        # Drop the message to lowercase to make searching easier
        message_content = message.content.lower()
        # Scan the string for the word words between square brackets using RegEx (I hate RegEx)

        match = re.search(r'\[(.*?)\]', message_content)
        if match:
            # Extract the matched string (without brackets)
            search_term = match.group(1)
            log.info(f"Item {search_term} requested by {message.author}")
            item_JSON = wowapihelper.search_for_item(search_term)

            responder = create_embedeed_message(tooltip_creator.create_tooltip(item_JSON))
            await message.channel.send(embed=responder[0], file=responder[1])


client.run(TOKEN)

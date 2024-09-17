# main.py - The NiceBot Entry Point
import datetime
import discord
import mysql.connector
import os
import re
from collections import defaultdict
from dotenv import load_dotenv

# Load in the Environmental Variables from the local .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('DISCORD_GUILD')
DB_USER = os.getenv('DATABASE_USER')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD')
DB_HOST = os.getenv('DATABASE_HOST')
DB_SCHEMA = os.getenv('DATABASE_SCHEMA')
BOT_PREFIX = os.getenv('BOT_PREFIX')
HELP_MESSAGE = os.getenv('HELP_MESSAGE')


# Local string formatted date method
def get_current_datetime():
    current_date_time = datetime.datetime.now()
    return current_date_time.strftime("%A %d %B %Y %X")


# Set up the Database Connection
def connect_to_database():
    config = {
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "database": DB_SCHEMA
    }
    try:
        db_connection = mysql.connector.connect(**config)
        return db_connection
    except:
        print("Connection to DB Failed")
        exit(1)


# Returns the number of times a user said Nice based on their User ID
def get_nice_count_for_user_id(id):
    db_connection = connect_to_database()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'SELECT * from nicecount where user_id = {id}')
    db_result = db_cursor.fetchone()
    return db_result


# Returns the last message from a user based on their User ID
def get_last_nice_message_for_user_id(id):
    db_connection = connect_to_database()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f'SELECT last_message, latest_nice from nicecount where user_id = {id}')
    db_result = db_cursor.fetchone()
    return db_result


# Creates a new database entry for a user
def create_new_nicecount_record(message):
    db_connection = connect_to_database()
    db_cursor = db_connection.cursor()
    sql = "INSERT INTO nicecount (display_name, count, latest_nice, last_message, user_id) values (%s,%s," \
          "%s,%s,%s) "
    values = (message.author.name, 1, get_current_datetime(), message.content, message.author.id)
    db_cursor.execute(sql, values)
    db_connection.commit()


# Updates the user's database entry based on their User ID
def update_nicecount_record(message):
    user_nice_count = int(get_nice_count_for_user_id(message.author.id)[2])
    new_nice_count = str(user_nice_count + 1)
    db_connection = connect_to_database()
    db_cursor = db_connection.cursor()
    sql = f"UPDATE nicecount SET count=%s, latest_nice=%s, last_message=%s WHERE user_id " \
          f"= {message.author.id} "
    values = (new_nice_count, get_current_datetime(), message.content)
    db_cursor.execute(sql, values)
    db_connection.commit()


# Instantiate the Discord Client
client = discord.Client()


# The Client On_Ready event - This fires when the Bot connects to Discord and joins the Guild
@client.event
async def on_ready():
    # DEBUG PRINT - Checks that the Bot has successfully connected to the server
    guild = discord.utils.get(client.guilds, name=GUILD_NAME)
    print(f'{client.user} has connected to Discord and is in the following Guilds:\n'
          f'{guild.name} (id: {guild.id})'
          )
    # DEBUG PRINT - iterates over the list of members on the server
    guild_members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {guild_members}')


# Check server messages for the word 'Nice' and chastise the user who said it
@client.event
async def on_message(message):
    if message.guild:
        response = ""
        # Ignore our own messages
        if message.author == client.user:
            return
        command_detected = False
        # Check to see if the message is a command
        if message.content.startswith(f'{BOT_PREFIX}'):
            # If it is a command then do the following
            command_detected = True
            if command_detected:
                # Nice Count Command
                if message.content.startswith(f'{BOT_PREFIX}nicecount'):
                    # Check to see if the command message mentions another user, and if it does treat only the first
                    # user mention as important
                    if message.mentions:
                        # Check the database to see if the mentioned user has a record
                        db_result = get_nice_count_for_user_id(message.mentions[0].id)
                        # If they don't have a record, report back
                        if db_result is None:
                            response = f'{message.mentions[0].mention} has never said the word Nice before! Well done ' \
                                       f'them. '
                        # If they do have a record, report back
                        else:
                            nice_count = db_result[2]
                            response = f'{message.mentions[0].mention}  has said Nice {nice_count} times.'
                    else:
                        db_result = get_nice_count_for_user_id(message.author.id)
                        if db_result is None:
                            response = f'{message.author.mention}, you have never said the word Nice before! Well ' \
                                       f'done you. '
                        else:
                            nice_count = db_result[2]
                            response = f'{message.author.mention}, you have said Nice {nice_count} times.'
                # Help Command - Sends a DM to the user with instructions
                if message.content.startswith(f'{BOT_PREFIX}help'):
                    dm_response = HELP_MESSAGE
                    # DM the user to asked for help with the dm_response, no need to spam the channel with this.
                    await message.author.send(dm_response)
                    return
                # Last Message Command - replied with the last Nice message for a given user
                if message.content.startswith(f'{BOT_PREFIX}lastnice'):
                    if message.mentions:
                        # Check the database to see if the mentioned user has a record
                        db_result = get_last_nice_message_for_user_id(message.mentions[0].id)
                        # If they don't have a record, report back
                        if db_result is None:
                            response = f'{message.mentions[0].mention} has never said the word Nice before! Well done ' \
                                       f'them. '
                        # If they do have a record, report back
                        else:
                            nice_message = f'[{db_result[1]}] - [{message.mentions[0].mention}]: {db_result[0]}'
                            response = f'The last message containing "Nice" that {message.mentions[0].mention}  said ' \
                                       f'was:\n\n' \
                                       f'{nice_message}.'
                    else:
                        db_result = get_last_nice_message_for_user_id(message.author.id)
                        if db_result is None:
                            response = f'{message.author.mention}, you have never said the word Nice before! Well ' \
                                       f'done you. '
                        else:
                            nice_message = f'[{db_result[1]}] - [{message.author.mention}]: {db_result[0]}'
                            response = f'The last message containing "Nice" that you said was:\n\n' \
                                       f'{nice_message}.'
        # If it's not a command, check the message for a Nice
        else:
            # Drop the message to lowercase to make searching easier
            message_content = message.content.lower()
            # Scan the string for the word Nice using RegEx (I hate RegEx)
            if re.search(r'\bnice', message_content):
                # Check the database to see if there is already an entry for this person
                db_result = get_nice_count_for_user_id(message.author.id)
                # If this is the first time they've said "nice" then chastise them, and log it in the DB
                if db_result is None:
                    response = (
                        f'{message.author.mention} has said NICE for the first time! Please be more descriptive in '
                        f'the future, nice is such a boring word...')
                    create_new_nicecount_record(message)
                # If they are a repeat offender, chastise them and report back on their transgressions
                else:
                    user_nice_count = int(get_nice_count_for_user_id(message.author.id)[2])
                    ordinal = int2ordinal(user_nice_count + 1)
                    response = f'{message.author.mention} has said NICE... AGAIN! This is the {ordinal} time ' \
                               f'they\'ve used it, the last time was {db_result[3]} '
                    update_nicecount_record(message)
        # Finally, respond to the channel if we have anything to say
        if response:
            await message.channel.send(response)


def int2ordinal(num):
    """
    Convert a natural number to an ordinal number.

    Args:
        num (int): natural number

    Returns:
        str: ordinal number, like 0th, 1st, 2nd,...

    Notes:
        Zero can be used as @num argument.
    """
    if not isinstance(num, int):
        raise TypeError(
            f"@num must be integer, but {num} was applied.")
    if num < 0:
        raise ValueError(
            f"@num must be over 0, but {num} was applied.")
    ordinal_dict = defaultdict(lambda: "th")
    ordinal_dict.update({1: "st", 2: "nd", 3: "rd"})
    q, mod = divmod(num, 10)
    suffix = "th" if q % 10 == 1 else ordinal_dict[mod]
    return f"{num}{suffix}"


client.run(TOKEN)

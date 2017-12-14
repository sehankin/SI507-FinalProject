import psycopg2
import psycopg2.extras
from config import *


# SOURCE: project6_code.py, taken in turn from lecture 11's twitter_database.py


def get_connection_and_cursor():
    try:
        if db_password != "":
            db_connection = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(db_name, db_user, db_password))
            print("Success connecting to database\n")
        else:
            db_connection = psycopg2.connect("dbname='{0}' user='{1}'".format(db_name, db_user))
    except:
        print("Unable to connect to the database. Check server and credentials.\n")
        sys.exit(1) # Stop running program if there's no db connection.
    db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return db_connection, db_cursor
db_connection, db_cursor = get_connection_and_cursor()

def setup_database(print_alert=False):
    db_cursor.execute("DROP TABLE IF EXISTS Abouts CASCADE")
    db_cursor.execute("DROP TABLE IF EXISTS Mentions CASCADE")
    db_cursor.execute("CREATE TABLE Abouts(ID SERIAL PRIMARY KEY, Character VARCHAR(40) UNIQUE, Articles_About Integer)")
    db_cursor.execute("CREATE TABLE Mentions(ID SERIAL PRIMARY KEY, Character VARCHAR(40) UNIQUE, Articles_Mentioned Integer)")
    db_connection.commit()
    if print_alert is True:
        print("TABLES CREATED\n")

def insert_character_counts_data_into_tables(character_counts_dct, print_alert=False):
    for character in character_counts_dct:
        character_abouts = character_counts_dct[character]["about"]
        character_mentions = character_counts_dct[character]["mentions"]
        db_cursor.execute("INSERT INTO Abouts(Character, Articles_About) VALUES(%s, %s) ON CONFLICT DO NOTHING", (character, character_abouts))
        if print_alert is True:
            print(character.upper() + " ABOUTS INSERTED INTO ABOUTS TABLE")
        db_cursor.execute("INSERT INTO Mentions(Character, Articles_Mentioned) VALUES(%s, %s) ON CONFLICT DO NOTHING", (character, character_mentions))
        if print_alert is True:
            print(character.upper() + " MENTIONS INSERTED INTO MENTIONS TABLE\n")
        db_connection.commit()

def query_and_return(query):
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    return results  # a list of dictionaries

import sqlite3
from sqlite3 import Error
import os

CON = None


def connect():
    """
    Function:
        connect
    Description:
        connects the program to db.sqlite database file
    Input:
         None
    Output:
        database connection
    """
    ''' connect program to database file db.sqlite '''
    global CON
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'db.sqlite')
    try:
        CON = sqlite3.connect(db_path)
        print("Connection to SQLite DB successful")
    except Error as err:
        print(f"The error '{err}' occurred when trying to connect to SQLite database")


def select_query(sql, args=()):
    """
    Function:
        select_query
    Description:
        Select query to return items from database
    Input:
         - args: selection criteria
    Output:
        Selects entries from database
    """

    cur = CON.cursor()
    return cur.execute(sql, args)


def delete_db():
    """
    Function:
        delete_db
    Description:
        Deletes the database
    Input:
         None
    Output:
        Database file is deleted
    """
    os.remove('db.sqlite')
    print("The SQLite database has been deleted")


def mutation_query(sql, args=()):
    """
    Function:
        mutation_query
    Description:
        Does a mutation on the database
    Input:
         - args: mutation criteria
    Output:
        Entries of the database is edited
    """
    cur = CON.cursor()
    cur.execute(sql, args)
    CON.commit()


def shutdown():
    """
    Function:
        shutdown
    Description:
        Disconnect the database connection
    Input:
         NOne
    Output:
        Bot disconnects from database
    """
    CON.close()
    print("The SQLite connection is closed")


def add_Tables(db):
    db.mutation_query('''
            CREATE TABLE IF NOT EXISTS ta_office_hours (
                guild_id    INT,
                ta          VARCHAR(50),
                day         INT,
                begin_hr    INT,
                begin_min   INT,
                end_hr      INT,
                end_min     INT
            )
        ''')

    db.mutation_query('''
            CREATE TABLE IF NOT EXISTS exams (
                guild_id    INT,
                title       VARCHAR(50),
                desc        VARCHAR(300),
                date        VARCHAR(10),
                begin_hr    INT,
                begin_min   INT,
                end_hr      INT,
                end_min     INT
            )
        ''')

    db.mutation_query('''
            CREATE TABLE IF NOT EXISTS assignments (
                guild_id    INT,
                title       VARCHAR(50),
                link        VARCHAR(300),
                desc        VARCHAR(300),
                date        VARCHAR(10),
                due_hr      INT,
                due_min     INT
            )
        ''')

    db.mutation_query('''
                CREATE TABLE IF NOT EXISTS custom_events (
                    guild_id    INT,
                    title       VARCHAR(50),
                    link        VARCHAR(300),
                    desc        VARCHAR(300),
                    date        VARCHAR(10),
                    due_hr      INT,
                    due_min     INT,
                    begin_hr    INT,
                    begin_min   INT,
                    end_hr      INT,
                    end_min     INT
                )
            ''')

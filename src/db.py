import psycopg2
from psycopg2 import sql
import json
import datetime

postgres_settings = json.load(open('servers.json'))['servers']['postgres']

# table_name = "clspeed_{0}".format(str(datetime.date.today())).replace("-","_")
table_name = "clspeed"

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = sql.SQL = (
        """
        CREATE TABLE {0} (
            speed DECIMAL,
            street VARCHAR(255),
            city VARCHAR(255),
            state VARCHAR(2),
            zip INTEGER,
            emm_lat decimal(12,10),
            emm_lng decimal(12,10),
            emm_acc VARCHAR(20)
        )
        """.format(table_name))
    conn = None
    try:
        # read the connection parameters
        # connect to the PostgreSQL server

        conn = psycopg2.connect(host=postgres_settings['host'],
                                database="clspeed",
                                user="clspeed",
                                password="clspeed")
        cur = conn.cursor()
        # create table one by one
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def write_entry(speed, entry):
    commands = sql.SQL = (
        """
        INSERT INTO {0} (speed, street, city, state, zip, emm_lat, emm_lng, emm_acc)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """.format(table_name))
    conn = None
    try:
        # read the connection parameters
        # connect to the PostgreSQL server

        conn = psycopg2.connect(host=postgres_settings['host'],
                                database="clspeed",
                                user="clspeed",
                                password="clspeed")
        cur = conn.cursor()
        # create table one by one
        cur.execute(commands, (speed,
                               entry['street'],
                               entry['city'],
                               entry['state'],
                               entry['zip'],
                               entry['emm_lat'],
                               entry['emm_lng'],
                               entry['emm_acc']))
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()

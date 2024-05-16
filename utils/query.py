import psycopg2
from psycopg2 import Error
from django.conf import settings
from django.db import connection
from collections import namedtuple
from psycopg2.extras import RealDictCursor
from django.db import DatabaseError, IntegrityError, transaction


try : 
    connection = psycopg2.connect(
        dbname='postgres',
        user='postgres.zdigjyodrdhsvdsdvuvo',
        password='Pacilflixjayajayajaya',
        host='aws-0-ap-southeast-1.pooler.supabase.com',
        port='5432'
    )
     # Create a cursor to perform database operations
    cursor = connection.cursor()
    print("Connected to the database")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

def map_cursor(cursor):
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def query(query_str: str, params=None):
    hasil = []
    with connection.cursor() as cursor:
        try:
            cursor.execute("SET SEARCH_PATH TO PacilFlix")
        except Exception as e:
            hasil = [str(e)]  # Convert the error message to a list
            connection.rollback()

        try:
            cursor.execute(query_str, params)  # Pass params to the query

            hasil = map_cursor(cursor)

        except Exception as e:
            hasil = [str(e)]  # Convert the error message to a list
            connection.rollback()

    return hasil

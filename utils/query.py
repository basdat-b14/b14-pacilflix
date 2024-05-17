import psycopg2
from psycopg2 import Error
from django.conf import settings
from django.db import connection
from collections import namedtuple
from psycopg2.extras import RealDictCursor
from django.db import DatabaseError, IntegrityError


try : 
    connection = psycopg2.connect(
        dbname='postgres',
        user='postgres.zdigjyodrdhsvdsdvuvo',
        password='Pacilflixjayajayajaya',
        host='aws-0-ap-southeast-1.pooler.supabase.com',
        port='5432'
    )
     # Create a cursor to perform database operations
    connection.autocommit = True
    cursor = connection.cursor()
    print("Connected to the database")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

def map_cursor(cursor):
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    # return [nt_result(*row) for row in cursor.fetchall()]
    return [dict(row) for row in cursor.fetchall()]

def query(query_str: str):
    hasil = []
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SET SEARCH_PATH TO PacilFlix")
        try:
            cursor.execute(query_str)

            if query_str.strip().upper().startswith("SELECT"):
                # ga eror return
                hasil = map_cursor(cursor)

            else:
                hasil = cursor.rowcount
                connection.commit()
        except Exception as e:

            hasil = [str(e)]  # Convert the error message to a list
            connection.rollback()

    return hasil


def connectdb(func):
    def wrapper(request):
        tem = ""
        with connection.cursor() as cursor:
            tem = func(cursor, request)
        return tem
    return wrapper
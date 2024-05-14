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
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

def map_cursor(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [dict(row) for row in cursor.fetchall()]

# def query(query_str: str):
#     hasil = []
#     with connection.cursor(cursor_factory=RealDictCursor) as cursor:
#         try:
#             # Ensure the search path is set correctly
#             cursor.execute("SET search_path TO PacilFlix")
#             cursor.execute(query_str)

#             if query_str.strip().upper().startswith("SELECT"):
#                 # Return results for SELECT queries
#                 hasil = map_cursor(cursor)
#             else:
#                 # Return row count for INSERT, UPDATE, DELETE
#                 hasil = cursor.rowcount
#                 connection.commit()
#         except Exception as e:
#             # Handle unexpected errors
#             hasil = str(e)

#     return hasil


def query(query_str: str):
    hasil = []
    # tmp = connection.cursor()
    with connection.cursor() as cursor:
        try:
            cursor.execute("SET SEARCH_PATH TO PacilFlix")
        except Exception as e:
            hasil = e
            connection.rollback()
            # cursor = tmp


        try:
            cursor.execute(query_str)

            if query_str.strip().lower().startswith("select"):
                # Kalau ga error, return hasil SELECT
                hasil = map_cursor(cursor)
            else:
                # Kalau ga error, return jumlah row yang termodifikasi oleh INSERT, UPDATE, DELETE
                hasil = cursor.rowcount
                # Buat commit di database
                connection.commit()
        except Exception as e:
            # Ga tau error apa
            hasil = e
            connection.rollback()

    return hasil

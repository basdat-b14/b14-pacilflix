from django.http import HttpResponseServerError
import psycopg2
from django.shortcuts import redirect, render
from psycopg2.extras import RealDictCursor




def daftar_unduhan_view(request): 
    return render(request, 'Daftar_Unduhan.html')

def daftar_favorit_view(request): 
    return render(request, 'Daftar_Favorit.html')

def contributors_list(request):
    if not request.session.get('is_authenticated'):
        return redirect('main:login_view')  # Redirect ke login kalo engga authenticated

    query = """
        SELECT c.nama, c.jenis_kelamin, c.kewarganegaraan, 
               array_to_string(array_agg(DISTINCT roles.role ORDER BY roles.role), ', ') AS roles
        FROM "CONTRIBUTORS" c
        LEFT JOIN (
            SELECT id, 'sutradara' AS role FROM "SUTRADARA"
            UNION
            SELECT id, 'penulis skenario' AS role FROM "PENULIS_SKENARIO"
            UNION
            SELECT id, 'pemain' AS role FROM "PEMAIN"
        ) roles ON c.id = roles.id
        GROUP BY c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan
    """
    contributors, success = execute_query(query)
    if not success:
        return HttpResponseServerError("Failed to fetch contributors")

    for contributor in contributors:
        contributor['jenis_kelamin'] = 'Laki - laki' if contributor['jenis_kelamin'] == 0 else 'Perempuan'
        contributor['roles'] = [role.capitalize() for role in contributor['roles'].replace(', ', ',').split(',')]
    
    return render(request, 'Daftar_Kontributor.html', {'contributors': contributors})

def execute_query(query, params=None):
    connection = get_connection()
    if connection is None:
        return {"error": "Connection to database failed"}, False
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SET search_path TO "PacilFlix" """)
            cursor.execute(query, params)
            if query.strip().lower().startswith('select'):
                results = cursor.fetchall()
                return results, True
            connection.commit()
            return {"message": "Query executed successfully"}, True
    except Exception as e:
        connection.rollback()
        return str(e), False
    finally:
        connection.close()


def get_connection():
    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres.zdigjyodrdhsvdsdvuvo',
            password='Pacilflixjayajayajaya',
            host='aws-0-ap-southeast-1.pooler.supabase.com',
            port='5432'
        )
        return connection
    except psycopg2.Error as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        return None




from django.shortcuts import render
from django.db import connection
from utils.query import query
from django.http import JsonResponse,  HttpResponseRedirect, HttpResponse
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from media_tayangan.views import tayangan_view
import json
from psycopg2 import errors
from django.db import connection, IntegrityError



from django.http import HttpResponseServerError
import psycopg2
from django.shortcuts import redirect, render
from psycopg2.extras import RealDictCursor





def daftar_unduhan_view(request):
   

    username = request.session.get('username')
    print(username)
    with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT
                            tayangan.id, 
                            tayangan.judul AS nama_tayangan, 
                            t.username, 
                            t.timestamp
                        FROM 
                            "PacilFlix"."TAYANGAN_TERUNDUH" AS t
                        JOIN 
                            "PacilFlix"."TAYANGAN" tayangan 
                        ON 
                            t.id_tayangan = tayangan.id
                        WHERE 
                            t.username = %s
                        ORDER BY 
                            t.timestamp DESC;
                    """, [username])
                    daftar_unduhan = cursor.fetchall()
                    print(daftar_unduhan)
                   
            
 

    # Convert list of tuples to list of dictionaries
    daftar_unduhan_dicts = [
        {'id_tayangan': row[0],'nama_tayangan': row[1], 'username' : row[2], 'timestamp': row[3]} for row in daftar_unduhan
    ]
    

    context = {
        'daftar_unduhan': daftar_unduhan_dicts
    }
    return render(request, 'Daftar_Unduhan.html', context)
        

def daftar_favorit_view(request): 

    username = request.session.get('username')
    with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT judul, timestamp
                        FROM "PacilFlix"."DAFTAR_FAVORIT"
                        WHERE username = %s;
                    """, [username])
                    daftar_favorit = cursor.fetchall()
                    
    daftar_favorit_dicts = [
        {'judul': row[0],'timestamp': row[1]} for row in daftar_favorit
    ]
    
    context = {
        'daftar_favorit' : daftar_favorit_dicts
    }
    print(daftar_favorit_dicts)
                    
                    
    return render(request, 'Daftar_Favorit.html', context)



  
       
@csrf_exempt
def delete_unduhan(request, nama_tayangan, username, id_tayangan):
    try:   
        with connection.cursor() as cursor:
            print('here1')
            
            cursor.execute("""
                DELETE FROM "PacilFlix"."TAYANGAN_TERUNDUH"
                WHERE id_tayangan = %s AND username = %s
            """, [id_tayangan, username])
            print('here')
            
           

        
        # if result != 0:
        #     print("trigger terpanggil")
        #     raise JsonResponse({'success': False , 'message':'Belum 1 hari.'})
        # else:
        #     print("trigger tidak terpanggil")
        #     return JsonResponse({'success': True , 'message':'Yeay'})
        # return JsonResponse({'success': True , 'message':'Sudah 1 hari.'})
        return HttpResponse('sudah 1 hari', status=200)
          
    except:
        print('trigger panggil')
        # return JsonResponse({'success': False , 'message':'Belum 1 hari.'})
        return HttpResponse(' kurang 1 hari', status=400)
        
        

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




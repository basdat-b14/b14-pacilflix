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





# Create your views here.
def contributor_list_view(request):
    return render(request, 'Daftar_Kontributor.html')

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
        
        
import psycopg2
from django.shortcuts import redirect, render

from main.views import execute_query




def daftar_unduhan_view(request): 
    return render(request, 'Daftar_Unduhan.html')

def daftar_favorit_view(request): 
    return render(request, 'Daftar_Favorit.html')



# def contributors_list(request):
#     if not request.session.get('is_authenticated', False):
#         # If the user is not authenticated, return a forbidden response
#         return HttpResponseForbidden('You must be logged in to access this page')
#     # Query untuk mendapatkan daftar kontributor dan peran mereka
#     query = """
#         SELECT c.nama, c.jenis_kelamin, c.kewarganegaraan, CASE
#             WHEN p.id IS NOT NULL THEN 'Penulis Skenario'
#             WHEN su.id IS NOT NULL THEN 'Sutradara'
#             WHEN pe.id IS NOT NULL THEN 'Pemain'
#             ELSE 'Other'
#         END AS role
#         FROM "CONTRIBUTORS" c
#         LEFT JOIN "PENULIS_SKENARIO" p ON c.id = p.id
#         LEFT JOIN "PEMAIN" pe ON c.id = pe.id
#         LEFT JOIN "SUTRADARA" su ON c.id = su.id
#     """
    
#     # Menjalankan query menggunakan fungsi eksekusi yang telah ditentukan
#     contributors, success = execute_query(query)
#     print(contributors)
#     if not success:
#         # Handle gagalnya eksekusi query
#         return JsonResponse({'error': 'Failed to fetch contributors'}, status=500)
    
#     # Mengkonversi jenis kelamin dari integer ke string yang lebih deskriptif
#     for contributor in contributors:
#         contributor['jenis_kelamin'] = 'Male' if contributor['jenis_kelamin'] == 0 else 'Female'

#     # Mengembalikan response dalam format JSON
#     return JsonResponse({"contributors": contributors})


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
        return render(request, 'error_page.html', {'message': 'Failed to fetch contributors'})

    for contributor in contributors:
        contributor['jenis_kelamin'] = 'Laki - laki' if contributor['jenis_kelamin'] == 0 else 'Perempuan'
        contributor['roles'] = [role.capitalize() for role in contributor['roles'].replace(', ', ',').split(',')]
    
    return render(request, 'Daftar_Kontributor.html', {'contributors': contributors})



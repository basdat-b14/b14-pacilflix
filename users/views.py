from datetime import timedelta, datetime
from venv import logger
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from main.views import execute_query, is_authenticated
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now






def buy_package(request, package_type):
    if not request.session.get('is_authenticated'):
        return redirect('main:login_view')  # Redirect ke login kalo engga authenticated
    
    if request.method == 'POST':
        metode_pembayaran = request.POST.get('metode_pembayaran')
        username = request.session.get('username')
        start_date_time = now().strftime('%Y-%m-%d %H:%M:%S')
        end_date_time = (now() + timedelta(days=30)).replace(hour=23, minute=59, second=59, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')  # end date based on tk 1, 1 bulan
        # end_date_time = (now() + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')


        # cek entry exists
        check_query = """
        SELECT 1 FROM "PacilFlix"."TRANSACTIONS"
        WHERE "username" = %s AND "start_date_time" = %s;
        """
        exists, _ = execute_query(check_query, (username, start_date_time))
        if exists:
            logger.error(f"Entry already exists for Username: {username}, Start Date: {start_date_time}")
        else:
            # insert bakal ngetrigger subscription_trigger
            transaction_query = """
                INSERT INTO "PacilFlix"."TRANSACTIONS" ("username", "start_date_time", "end_date_time", "nama_paket", "metode_pembayaran", "timestamp_pembayaran")
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            hasil, success = execute_query(transaction_query, (username, start_date_time, end_date_time, package_type, metode_pembayaran, now().strftime('%Y-%m-%d %H:%M:%S')))
            print(hasil)
            print(success)

        return redirect('users:subscription_page')  # Redirect ke langganan.html

    # Else, show halaman package selection
    package_info, success = execute_query("""
        SELECT p."nama", p."harga", p."resolusi_layar", string_agg(dp."dukungan_perangkat", ', ') AS "dukungan_perangkat"
        FROM "PacilFlix"."PAKET" p
        LEFT JOIN "PacilFlix"."DUKUNGAN_PERANGKAT" dp ON p."nama" = dp."nama_paket"
        WHERE p."nama" = %s
        GROUP BY p."nama", p."harga", p."resolusi_layar";
    """, (package_type,))
    
    if success and package_info:
        # Extract paketnya
        package_dict = package_info[0]
    else:
        package_dict = None  # handle kalo query gagal, ato engga ada paket

    return render(request, 'Beli_Paket.html', {'package_info': package_dict})


# def dashboard_pengguna(request):
#     username = request.session.get('username')
#     password = request.session.get('password')

#     print(f"Username from session: {username}")  # Debug: Cetak username dari sesi
#     print(f"Password from session: {password}")  # Debug: Cetak password dari sesi

#     if not (username and password):
#         return HttpResponse("Unauthorized", status=401)

#     pengguna_data = query("SELECT * FROM pengguna WHERE username = %s", (username,))
    


#     print(f"Pengguna data: {pengguna_data}")  # Debug: Cetak data pengguna

#     # Jika terjadi kesalahan saat query, redirect ke halaman login
#     if isinstance(pengguna_data[0], str):
#         return redirect("/login")

#     if pengguna_data and check_password(password, pengguna_data[0].password):
#         pengguna = pengguna_data[0]
#         username = pengguna.username
#         password = pengguna.password
#         negara_asal = pengguna.negara_asal

#         context = {
#             "username": username,
#             "password": password,
#             "negara_asal": negara_asal,
#         }
#         return render(request, 'DashboardPengguna.html', context)  # Ganti redirect dengan render
#     else:
#         return HttpResponse("Unauthorized", status=401)


# Create your views here.
def dashboard_pengguna(request):
    username = request.session["username"]
    password = request.session["password"]

    # negara_asal = query("""SELECT negara_asal FROM PENGGUNA WHERE 
    #                 username='{}' AND password='{}';
    #                 """.format(username, password))[0]["negara_asal"]
    
    context = {
        "username": username,
        "password": password,
        # "negara_asal": negara_asal
    }
    return render(request, 'Dashboard_Pengguna.html', context)

@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = make_password(request.POST.get('password'))
        negara_asal = request.POST.get('negara_asal')

        # Update data pengguna di database
        query(f"""UPDATE pengguna SET username=%s, password=%s, negara_asal=%s WHERE username=%s""", (username, password, negara_asal, request.session["username"]))

        # Update data pengguna di sesi
        request.session["username"] = username
        request.session["password"] = password

    return redirect('users:dasboard_pengguna')


# def subscription_history(request):
#     if not request.session.get('is_authenticated'):
#         return redirect('login_view')  # Redirect to login if the user is not authenticated

#     username = request.session.get('username')
#     if username:
#         query = """
#             SELECT t."nama_paket", t."start_date_time", t."end_date_time", t."metode_pembayaran", t."timestamp_pembayaran", p."harga" as "total_pembayaran"
#             FROM "PacilFlix"."TRANSACTIONS" t
#             JOIN "PacilFlix"."PAKET" p ON t."nama_paket" = p."nama"
#             WHERE t."username" = %s
#             ORDER BY t."start_date_time" ASC;
#         """
#         subscriptions, success = execute_query(query, (username,))
#         print(subscriptions)  # This print statement helps in debugging to see the fetched data
#     else:
#         subscriptions = []  # Set to empty list if no username found in session

#     return render(request, 'Langganan.html', {'subscriptions': subscriptions})

# def view_packages(request):
#     if not request.session.get('is_authenticated'):
#         return redirect('login_view')  # Redirect to login if the user is not authenticated

#     query = """
#         SELECT p."nama", p."harga", p."resolusi_layar", string_agg(dp."dukungan_perangkat", ', ') AS "dukungan_perangkat"
#         FROM "PacilFlix"."PAKET" p
#         LEFT JOIN "PacilFlix"."DUKUNGAN_PERANGKAT" dp ON p.nama = dp.nama_paket
#         GROUP BY p.nama, p.harga, p.resolusi_layar
#         ORDER BY p.harga;
#     """
#     packages, success = execute_query(query)
#     print(packages)
#     if not success:
#         packages = []  # Fallback to an empty list if the query fails

#     return render(request, 'Langganan.html', {'packages': packages})



def combined_subscription_view(request):
    if not request.session.get('is_authenticated'):
        return redirect('main:login_view')  # Redirect ke login kalo engga authenticated

    username = request.session.get('username')
    packages = []
    subscriptions = []

    current_time = now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"Current server time for query: {current_time}")

    # Query buat opsi packages
    package_query = """
        SELECT p."nama", p."harga", p."resolusi_layar", string_agg(dp."dukungan_perangkat", ', ') AS "dukungan_perangkat"
        FROM "PacilFlix"."PAKET" p
        LEFT JOIN "PacilFlix"."DUKUNGAN_PERANGKAT" dp ON p."nama" = dp."nama_paket"
        GROUP BY p."nama", p."harga", p."resolusi_layar"
        ORDER BY p."harga";
    """
    packages, package_success = execute_query(package_query)

    # Query buat ambil subscription history
    if username:
        subscription_query = """
            SELECT t."nama_paket", t."start_date_time", t."end_date_time", t."metode_pembayaran", t."timestamp_pembayaran", p."harga" as "total_pembayaran"
            FROM "PacilFlix"."TRANSACTIONS" t
            JOIN "PacilFlix"."PAKET" p ON t."nama_paket" = p."nama"
            WHERE t."username" = %s
            ORDER BY t."start_date_time" ASC;
        """
        subscriptions, subscription_success = execute_query(subscription_query, (username,))
    
    # Query buat ambil active subscription
    if username:
        active_subscription_query = """
            SELECT t."nama_paket", t."start_date_time", t."end_date_time", t."metode_pembayaran", p."harga" as "total_pembayaran", p."resolusi_layar", STRING_AGG(dp."dukungan_perangkat", ', ') AS "dukungan_perangkat"
            FROM "PacilFlix"."TRANSACTIONS" t
            JOIN "PacilFlix"."PAKET" p ON t."nama_paket" = p."nama"
            LEFT JOIN "PacilFlix"."DUKUNGAN_PERANGKAT" dp ON p."nama" = dp."nama_paket"
            WHERE t."username" = %s  AND t."end_date_time" > %s
            GROUP BY t."nama_paket", t."start_date_time", t."end_date_time", t."metode_pembayaran", p."harga", p."resolusi_layar"
            ORDER BY t."start_date_time" DESC 
            LIMIT 1;
        """
        active_subscription, active_subscription_success = execute_query(active_subscription_query, (username, current_time))
        print(f"Active subscription query returned: {active_subscription}")

    # Handle kalo ga ada
    if not package_success:
        packages = []  
    if not subscription_success:
        subscriptions = []  
    if not active_subscription_success:
        active_subscription = None

    # Rendering dari html untuk langganan html
    return render(request, 'Langganan.html', {'packages': packages, 'subscriptions': subscriptions, 'active_subscription': active_subscription[0] if active_subscription else None})



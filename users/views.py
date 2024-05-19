from datetime import timedelta, datetime
from venv import logger
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
import psycopg2
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from psycopg2.extras import RealDictCursor



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


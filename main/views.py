from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.db import connection
from django.contrib.auth.hashers import make_password, check_password
import psycopg2
from utils.query import query 
from psycopg2.extras import RealDictCursor
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from media_tayangan.views import tayangan_view
import json



def show_main(request):
    return render(request, 'main.html')  


def login_view(request):

    if request.session.get('is_authenticated'):
        return redirect(reverse('media_tayangan:tayangan_view'))
    
    if request.method == 'POST':
        response = login(request)
        if response.status_code == 200:
            return redirect(reverse('media_tayangan:tayangan_view')) # login sukses
        else:
            return render(request, "login.html")  # login gagal
    else:
        # stage awal
        return render(request, "login.html")
    
def register(request):
  if request.method != 'POST':
    return render(request, 'register.html')
   

def check_session(request):
    '''Check apakah info user masih ada di session atau belum'''
    try:
        request.session["username"]
        request.session["password"]
        return True
    except KeyError:
        return False
    
def is_authenticated(request):
    try:
        request.session["username"]
        return True
    except KeyError:
        return False

def get_session_data(request):
    if not is_authenticated(request):
        return {}
    try:
        return {"username": request.session["username"]}
    except:
        return {}

@csrf_exempt
def login(request):
    next = request.GET.get("next")
    if request.method != "POST":
        return login_view(request)
    try:
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        
        query = f"""SELECT * FROM "PENGGUNA" WHERE username = '{username}' LIMIT 1"""
        user, success = execute_query(query)
        print (user)
        if not success or not user:
            messages.error(request, 'Username atau Password Anda Salah. Silahkan Coba lagi!')
            return JsonResponse({'error': 'Authentication failed'}, status=401)
        
        # Assuming password is plain text for example; use hashed passwords in production
        if user[0]['password'] != password:
            messages.error(request, 'Username atau Password Anda Salah. Silahkan Coba lagi!')
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        # Log the user in using Django's session framework
        request.session['username'] = username  # Store username in session
        request.session['is_authenticated'] = True 
        return JsonResponse({'success': 'User successfully logged in'}, status=200)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def logout(request):
    next = request.GET.get("next")

    if not is_authenticated(request):
        return redirect("/")

    request.session['is_authenticated'] = False
    request.session.flush()
    request.session.clear_expired()

    if next != None and next != "None":
        return redirect(next)
    else:
        return redirect("/")

def get_existing_usernames():
    query = "SELECT username FROM PENGGUNA;"
    results, success = execute_query(query)
    if success:
        return [pengguna['username'] for pengguna in results]
    return []

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        negara_asal = request.POST.get('negara_asal')


        # Memeriksa apakah semua field sudah diisi
        if not (username and password and negara_asal):
            # Jika tidak, kembalikan response BadRequest
            messages.error(request, 'Semua field harus diisi!')
            return render(request, "register.html")
        try:
            # Check if the username already exists
            query = f"""SELECT * FROM "PENGGUNA" WHERE username = %s LIMIT 1"""
            user, success = execute_query(query, (username,))
            
            if success and user:
                messages.error(request, 'Username sudah pernah terdaftar')
                return render(request, "register.html")

            # Insert the new user into the database
            query = """INSERT INTO "PENGGUNA" (username, password, negara_asal) VALUES (%s, %s, %s)"""
            result, success = execute_query(query, (username, password, negara_asal))
            if success:
                messages.success(request, 'Berhasil mendaftar!')
                return redirect('/login/')
            else:
                raise Exception(result)  # Raise an exception if the query execution was not successful

        except Exception as e:
            messages.error(request, 'Gagal mendaftarkan pengguna, coba lagi!')
            return render(request, "register.html", {'message': 'Gagal mendaftarkan pengguna, coba lagi!'})

    return render(request, "register.html", {'message': ""})


# Utility function for executing queries
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


def is_authenticated(request):
    return request.session.get("is_authenticated", False)

def get_session_data(request):
    if not is_authenticated(request):
        return {}
    return {"username": request.session.get("username")}
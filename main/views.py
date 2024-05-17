from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import psycopg2
from psycopg2.extras import RealDictCursor


# Create your views here.
def show_main(request):
    return render(request, 'main.html')

def register(request):
    return ''

def login_view(request):
    if request.method == 'POST':
        response = login(request)
        if response.status_code == 200:
            return redirect(reverse('main:show_main')) # login sukses
        else:
            return render(request, "login.html")  # login gagal
    else:
        # stage awal
        return render(request, "login.html")


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
        print("Error while connecting to PostgreSQL", error)
        return None

def execute_query(query):
    connection = get_connection()
    if connection is None:
        return {"error": "Connection to database failed"}, False
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SET search_path TO "PacilFlix" """)
            cursor.execute(query)
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

@require_http_methods(["POST"])
def login(request):
    try:
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        
        query = f"""SELECT * FROM "PENGGUNA" WHERE username = '{username}' LIMIT 1"""
        user, success = execute_query(query)
        print (user)
        if not success or not user:
            return JsonResponse({'error': 'Authentication failed'}, status=401)
        
        # Assuming password is plain text for example; use hashed passwords in production
        if user[0]['password'] != password:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        # Log the user in using Django's session framework
        request.session['username'] = username  # Store username in session
        request.session['is_authenticated'] = True 
        return JsonResponse({'success': 'User successfully logged in'}, status=200)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@require_http_methods(["POST"])
def logout_view(request):
    # This will clear the user's session and log them out.
    request.session['is_authenticated'] = False  
    request.session.flush()
    
    return redirect(reverse('main:show_main'))


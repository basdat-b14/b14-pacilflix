from django.shortcuts import render
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from media_tayangan.views import tayangan_view
from .models import UserProfile
from django.contrib.auth.models import User

from django.contrib import messages

# Create your views here.
def show_main(request):
    return render(request, 'main.html')

def register(request):
  if request.method != 'POST':
    return render(request, 'register.html')
  

def login_view(request):
  return render(request, "login.html")


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
    if is_authenticated(request):
        return redirect('media_tayangan:tayangan_view')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Debugging: Print username yang diterima dari form login
        print("Username yang diinput:", username)

        # Verifikasi pengguna
        pengguna = query(f"""SELECT * FROM pengguna WHERE username='{username}' and password='{password}'""")
        flag = is_authenticated(request)

        if pengguna != [] and not flag:
            request.session["username"] = username
            request.session["password"] = password
            request.session['is_authenticated'] = True  # Setel status pengguna yang sudah masuk
            request.session.set_expiry(500)
            request.session.modified = True

            if next:
                return redirect(next)
            else:
                # Redirect ke halaman tayangan_view jika berhasil login
                return redirect('media_tayangan:tayangan_view')

    return render(request, 'login.html', {'user': get_session_data(request)})


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        negara_asal = request.POST.get('negara_asal')

        print("Username:", username)  # Debug: Cetak nilai username
        print("Password:", password)  # Debug: Cetak nilai password
        print("Negara Asal:", negara_asal)  # Debug: Cetak nilai negara_asal

        # Cek apakah username sudah terdaftar
        check_username = query(f"""SELECT * FROM PENGGUNA WHERE username = '{username}'""")

        # Jika terjadi kesalahan saat query, redirect ke halaman login
        if isinstance(check_username[0], str):
            return redirect("/login")

        # Jika tidak ada username yang cocok, tambahkan ke basis data
        if not check_username:
            try:
                query(f"""INSERT INTO PENGGUNA VALUES ('{username}', '{password}', '{negara_asal}')""")
                print("User berhasil ditambahkan ke basis data")  # Debug: Cetak jika user berhasil ditambahkan
                return redirect('/login/')
            except Exception as e:
                print("Error:", e)  # Debug: Cetak pesan kesalahan saat eksekusi query
                context = {'message': "Gagal mendaftarkan pengguna"}
                return render(request, "register.html", context)
        else:
            print("Username sudah terdaftar")  # Debug: Cetak jika username sudah terdaftar
            context = {'message': "Username sudah pernah terdaftar"}
            return render(request, "register.html", context)
    
    context = {'message': ""}
    return render(request, "register.html", context)




def logout(request):
    next = request.GET.get("next")

    if not is_authenticated(request):
        return redirect("/")

    request.session.flush()
    request.session.clear_expired()

    if next != None and next != "None":
        return redirect(next)
    else:
        return redirect("/")
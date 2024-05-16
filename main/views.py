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
import uuid


from .models import UserProfile
# Create your views here.
def show_main(request):
    return render(request, 'main.html')

def register(request):
    print("masuk regist")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("bisa buat akun")
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('main.html')
        else:
            print("gabisa buat akun")
            messages.error(request, "Invalid registration credentials. Please try again.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# def login(request):
#     print("masuk login")
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('main.html')
#         else:
#             messages.error(request, "Invalid login credentials. Please try again.")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

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


# @csrf_exempt
# def login(request):
#     next = request.GET.get("next")
#     if request.method != "POST":
#         return login_view(request)

#     username = ''
#     password = ''

#     if 'username' in request.session and 'password' in request.session:
#         username = request.session['username']
#         password = request.session['password']
#     else:
#         username = request.POST['username']
#         password = request.POST['password']

#     # Memeriksa username dan password di dalam tabel Pengguna
#     print(username)
#     print(password)
    
#     pengguna = authenticate_user("SELECT * FROM PENGGUNA WHERE username = %s AND password = %s", (username, password))
#     print(pengguna)

#     if not pengguna:
#         context = {'fail': True}
#         return render(request, "login.html", context)

#     request.session["username"] = pengguna['username']
#     request.session["password"] = pengguna['password']
#     request.session["id_tayangan"] = pengguna['id_tayangan']
#     request.session["negara_asal"] = pengguna['negara_asal']
#     request.session.set_expiry(0)
#     request.session.modified = True

#     if next and next != "None":
#         return redirect(next)
#     else:
#         # redirect to dashboard
#         if pengguna['negara_asal'] == 'Indonesia':
#             return redirect('/indonesia')
#         elif pengguna['negara_asal'] == 'Inggris':
#             return redirect('/inggris')
#         else:
#             return redirect('/global')


def is_authenticated(request):
    try:
        request.session["username"]
        return True
    except KeyError:
        return False

@csrf_exempt
def login(request):
    next = request.GET.get("next")
    if is_authenticated(request):
        return redirect("main.html")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Memeriksa username dan password di dalam tabel Pengguna
        pengguna = query(f"""SELECT * FROM pengguna WHERE username='{username}' and password='{password}'""")
        flag = is_authenticated(request)
        if pengguna != [] and not flag:
            request.session["username"] = username
            request.session["password"] = password
            # request.session["negara_asal"] = negara_asal
            request.session.set_expiry(500)
            request.session.modified = True
            if next != None and next != "None":
                return redirect(next)
            else:
                # Mengarahkan pengguna ke dashboard
                return redirect("main.html")
    return render(request, 'login.html')
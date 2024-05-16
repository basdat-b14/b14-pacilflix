from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from utils.query import query
from django.views.decorators.csrf import csrf_exempt

def subscription_page(request):
    return render(request, 'Langganan.html')

def buy_package(request, package_type):
    packages = {
        'basic': {'name': 'Basic', 'price': '50000', 'resolution': '720p', 'support': 'Mobile, Tablet'},
        'standard': {'name': 'Standard', 'price': '80000', 'resolution': '1080p', 'support': 'Mobile, Tablet, Computer'},
        'premium': {'name': 'Premium', 'price': '120000', 'resolution': '4K', 'support': 'Mobile, Tablet, Computer, TV'}
    }
    package_info = packages.get(package_type)
    return render(request, 'Beli_Paket.html', {'package': package_info})

def dashboard_pengguna(request):
    username = request.session.get('username')
    password = request.session.get('password')

    if not (username and password):
        return HttpResponse("Unauthorized", status=401)

    pengguna_data = query("SELECT * FROM pengguna WHERE username = %s", (username,))

    if pengguna_data and check_password(password, pengguna_data[0].password):
        pengguna = pengguna_data[0]
        username = pengguna.username
        password = pengguna.password
        negara_asal = pengguna.negara_asal

        context = {
            "username": username,
            "password": password,
            "negara_asal": negara_asal,
        }
        return render(request, 'DashboardPengguna.html', context)
    else:
        return HttpResponse("Unauthorized", status=401)

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

    return redirect('users:dashboardPengguna')

from django.shortcuts import render

# Create your views here.
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

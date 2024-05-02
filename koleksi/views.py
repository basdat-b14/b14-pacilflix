from django.shortcuts import render

# Create your views here.
def contributor_list_view(request):
    return render(request, 'Daftar_Kontributor.html')

def daftar_unduhan_view(request): 
    return render(request, 'Daftar_Unduhan.html')

def daftar_favorit_view(request): 
    return render(request, 'Daftar_Favorit.html')
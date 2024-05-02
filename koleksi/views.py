from django.shortcuts import render

# Create your views here.
def contributor_list_view(request):
    return render(request, 'Daftar_Kontributor.html')

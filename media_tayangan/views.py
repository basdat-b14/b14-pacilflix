from django.shortcuts import render

# Create your views here.
def trailer_view(request):
    return render(request, 'trailer.html')

def cari_trailer(request):
    return render(request, 'pencarian_trailer.html')

def tayangan_view(request):
    return render(request, 'tayangan.html')

def cari_tayangan(request):
    return render(request, 'pencarian_tayangan.html')

def film_view(request):
    return render(request, 'halaman_film.html')

def series_view(request):
    return render(request, 'halaman_series.html')

def episode_view(request):
    return render(request, 'halaman_episode.html')
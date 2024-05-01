from django.shortcuts import render

# Create your views here.
def trailer_view(request):
    return render(request, 'trailer.html')
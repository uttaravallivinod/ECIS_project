from django.shortcuts import render
from .models import Whether
import folium
from django.conf import settings

# Create your views here.

def home(request):
    locations=Whether.objects.all()
    map_pin=folium.Map()
    for location in locations:
        folium.Marker([location.location.y,location.location.x],tooltip='<b>this is '+location.city+' pin.').add_to(map_pin)
    #print(settings.TEMPLATES[0]['DIRS'][0])
    map_pin.save(settings.TEMPLATES[0]['DIRS'][0]+'\map.html')

    
    return render(request,'home.html')

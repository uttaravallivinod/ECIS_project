from django.shortcuts import redirect, render
from .models import Whether
import folium
from django.conf import settings
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point


# Create your views here.

def home(request):
    context=[]
    if request.method=='POST':
        city_name=request.POST['city']
        try:
            geo_locator=Nominatim(user_agent='ECSI_project')
            geo_data=geo_locator.geocode(city_name)
            latitude=geo_data.latitude
            longitude=geo_data.longitude
            coordinates=Point(latitude,longitude)
            whether_object=Whether.objects.create(location=coordinates)
            whether_object.save()

        except Exception as e:
            print(e)
            return redirect('/')
        latest_object=Whether.objects.latest('id')
        geo_info={}
        geo_info['latitude']=latest_object.location.x
        geo_info['longitude']=latest_object.location.y
        geo_info['city']=city_name
        context.append(geo_info)
        return render(request,'home.html',{'data':context})
        
    locations=Whether.objects.all()
    for location in locations:
        temp={}
        temp['latitude']=location.location.x
        temp['longitude']=location.location.y
        temp['city']=location.city
        context.append(temp)

    return render(request,'home.html',{'data':context})

from django.shortcuts import redirect, render
from requests.adapters import HTTPResponse
from .models import Whether
import folium
from django.conf import settings
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
import requests
import json
def home(request):
    key="f14c03d5b7874fe785e14744211709"
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
        try:
            url=f"http://api.weatherapi.com/v1/current.json?key={key} &q={geo_info['latitude']},{geo_info['longitude']}&aqi=no"
            geo_info['whether']=json.loads(requests.get(url)._content)
        except Exception as e:
            return HTTPResponse(e)
        context.append(geo_info)
        return render(request,'home.html',{'data':context})
    locations=Whether.objects.all().order_by('-date')[:5]
    for location in locations:
        temp={}
        temp['latitude']=location.location.x
        temp['longitude']=location.location.y
        try:
            url=f"http://api.weatherapi.com/v1/current.json?key={key} &q={temp['latitude']},{temp['longitude']}&aqi=no"
            temp['whether']=json.loads(requests.get(url)._content)
        except Exception as e:
            return HTTPResponse(e)
        context.append(temp)
    return render(request,'home.html',{'data':context,'info':'Recent '+str(len(context))+' location details:'})

from django.http import response
from django.test import TestCase
from whether_details.models import Whether
from django.contrib.gis.geos import Point
from django.urls import reverse

# Create your tests here.
class Testing_Models(TestCase):
    def setUp(self):
        Whether.objects.create(location=Point([32.9876,45.8765])).save()
        Whether.objects.create(location=Point([67.8768,98.5456])).save()
    def test_get_records(self):
        records=Whether.objects.all().count()
        self.assertEqual(records,2)
    def test_insert_records(self):
        Whether.objects.create(location=Point([54.5678,23.5994])).save()
        self.assertEqual(Whether.objects.all().count(),3)
    def test_delete_records(self):
        obj=Whether.objects.earliest('id')
        obj.delete()
        self.assertEqual(Whether.objects.all().count(),1)
class Testing_Urls(TestCase):
    def test_get_homepage(self):
        url='/'
        response=self.client.get(url)
        self.assertEqual(response.status_code,200)
    def test_view_checking(self):
        response=self.client.get(reverse('home_page'))
        self.assertEqual(response.status_code,200)





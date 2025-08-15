
from django.urls import path
from .views import index, robots, sitemap, test_view

urlpatterns = [
    path('', index, name='index'),
    path('robots.txt', robots, name='robots'),
    path('sitemap.xml', sitemap, name='sitemap'),
    path('test/', test_view, name='test_view'),
]


from django.urls import path
from .views import index, robots, sitemap

urlpatterns = [
    path('', index, name='index'),
    path('robots.txt', robots, name='robots'),
    path('sitemap.xml', sitemap, name='sitemap'),
]

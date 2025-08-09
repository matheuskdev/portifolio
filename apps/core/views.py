from django.shortcuts import render
from .models import *

def index(request):

    metadata = MetaData.objects.filter(is_active=True).first()
    hero = Hero.objects.filter(is_active=True).first()
    about = About.objects.filter(is_active=True).first()
    skillgroups = SkillGroup.objects.filter(is_active=True)
    projects = Project.objects.filter(is_active=True)
    contact = Contact.objects.filter(is_active=True).first()
    sections = Sections.objects.all().first()
    context = {
        'metadata': metadata, 'hero': hero, 'about': about,
        'skillgroups': skillgroups, 'projects': projects,
        'contact': contact, 'sections': sections
    }
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Message.objects.create(name=name, email=email, message=message)
        return render(request, 'main/index.html', context=context)

    return render(request, 'main/index.html', context=context)

def robots(request):
    return render(request, 'robots.txt', content_type='text/plain')

def sitemap(request):
    return render(request, 'sitemap.xml', content_type='text/xml')
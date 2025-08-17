from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import (
    MetaData, Hero, About, SkillGroup, Project, Contact, Sections, Footer, Message
)
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def index(request):

    metadata = MetaData.objects.filter(is_active=True).first()
    hero = Hero.objects.filter(is_active=True).first()
    about = About.objects.filter(is_active=True).first()
    skillgroups = SkillGroup.objects.filter(is_active=True)
    projects = Project.objects.filter(is_active=True)
    contact = Contact.objects.filter(is_active=True).first()
    sections = Sections.objects.all().first()
    footer = Footer.objects.all().first()
    context = {
        'metadata': metadata, 'hero': hero, 'about': about,
        'skillgroups': skillgroups, 'projects': projects,
        'contact': contact, 'sections': sections, 'footer': footer
    }
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            context['error'] = 'Todos os campos são obrigatórios.'
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('index')

        Message.objects.create(name=name, email=email, message=message)
        return render(request, 'main/index.html', context=context)

    return render(request, 'main/index.html', context=context)


@cache_page(60 * 60 * 24)  # 1 dia de cache
def robots(request):
    return render(request, 'main/robots.txt', content_type='text/plain')

@cache_page(60 * 60 * 24)
def sitemap(request):
    return render(request, 'main/sitemap.xml', content_type='application/xml')


@login_required
def test_view(request):
    return render(request, 'main/test.html')
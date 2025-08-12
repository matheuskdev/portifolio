from django.contrib import admin
from django.db import transaction
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from .models import *

# Filtros personalizados
class FilterActive(SimpleListFilter):
    title = 'Status'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Ativo'),
            ('0', 'Inativo'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(is_active=True)
        if self.value() == '0':
            return queryset.filter(is_active=False)

class FilterContent(SimpleListFilter):
    title = 'Possui Conteúdo'
    parameter_name = 'has_content'

    def lookups(self, request, model_admin):
        return (
            ('sim', 'Sim'),
            ('nao', 'Não'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'sim':
            return queryset.exclude(content__isnull=True).exclude(content__exact='')
        if self.value() == 'nao':
            return queryset.filter(content__isnull=True) | queryset.filter(content__exact='')

# Classe base para admin com funcionalidades comuns
class BaseAdmin(admin.ModelAdmin):
    """Classe base para admin com funcionalidades comuns"""

    def get_readonly_fields(self, request, obj=None):
        """Campos de data de criação e atualização são somente leitura"""
        campos = list(super().get_readonly_fields(request, obj))
        if hasattr(self.model, 'created_at'):
            campos.append('created_at')
        if hasattr(self.model, 'updated_at'):
            campos.append('updated_at')
        return campos

    def get_list_display(self, request):
        """Inclui ícone de status na listagem se o campo existir"""
        campos = list(super().get_list_display(request))
        if 'is_active' in [f.name for f in self.model._meta.fields]:
            if 'icone_status' not in campos:
                campos.append('icone_status')
        return campos

    def icone_status(self, obj):
        if hasattr(obj, 'is_active'):
            cor = 'green' if obj.is_active else 'red'
            return format_html(f'<span style="color: {cor}; font-size: 16px;">●</span>')
        return '-'
    icone_status.short_description = 'Status'

# Admin para modelos com instância única ativa
class AdminSingleton(BaseAdmin):
    """Admin para modelos que devem ter somente uma instância ativa"""

    def save_model(self, request, obj, form, change):
        with transaction.atomic():
            if obj.is_active:
                # Garante que só uma instância esteja ativa
                self.model.objects.update(is_active=False)
            super().save_model(request, obj, form, change)

    def get_actions(self, request):
        acoes = super().get_actions(request)
        # Desabilita ação de excluir múltiplos registros
        if 'delete_selected' in acoes:
            del acoes['delete_selected']
        return acoes

# Admin para MetaData
@admin.register(MetaData)
class MetaDataAdmin(AdminSingleton):
    list_display = ('title', 'preview_keywords', 'preview_description')
    list_filter = (FilterActive,)
    search_fields = ('title', 'description', 'keywords')

    fieldsets = (
        ('Informações SEO', {
            'fields': ('title', 'description', 'keywords'),
            'description': 'Configurações para otimização em motores de busca'
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )

    def preview_keywords(self, obj):
        if obj.keywords:
            texto = obj.keywords[:50] + ('...' if len(obj.keywords) > 50 else '')
            return format_html('<span title="{}">{}</span>', obj.keywords, texto)
        return format_html('<span style="color: #999;">Sem palavras-chave</span>')
    preview_keywords.short_description = 'Palavras-chave'

    def preview_description(self, obj):
        if obj.description:
            texto = obj.description[:60] + ('...' if len(obj.description) > 60 else '')
            return format_html('<span title="{}">{}</span>', obj.description, texto)
        return format_html('<span style="color: #999;">Sem descrição</span>')
    preview_description.short_description = 'Descrição'


# Admin para Hero
@admin.register(Hero)
class HeroAdmin(AdminSingleton):
    list_display = ('full_name', 'title', 'preview_greeting', 'preview_bio')
    list_filter = (FilterActive,)
    search_fields = ('full_name', 'title', 'greeting', 'bio')

    fieldsets = (
        ('Informações do Hero', {
            'fields': ('greeting', 'full_name', 'title'),
            'description': 'Conteúdo principal da seção hero na página inicial'
        }),
        ('Biografia', {
            'fields': ('bio',),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )

    def preview_greeting(self, obj):
        if obj.greeting:
            return format_html('<em>{}</em>', obj.greeting)
        return format_html('<span style="color: #999;">Sem saudação</span>')
    preview_greeting.short_description = 'Saudação'

    def preview_bio(self, obj):
        if obj.bio:
            texto = obj.bio[:80] + ('...' if len(obj.bio) > 80 else '')
            return format_html('<span title="{}">{}</span>', obj.bio, texto)
        return format_html('<span style="color: #999;">Sem biografia</span>')
    preview_bio.short_description = 'Biografia'

# Admin para About
@admin.register(About)
class AboutAdmin(AdminSingleton):
    list_display = ('contagem_palavras', 'preview_avatar')
    list_filter = (FilterActive,)
    search_fields = ('about',)

    fieldsets = (
        ('Conteúdo Sobre', {
            'fields': ('about',),
            'classes': ('wide',),
            'description': 'Conteúdo principal da seção sobre mim'
        }),
        ('Avatar', {
            'fields': ('avatar',),
            'description': 'Imagem do perfil para a seção sobre'
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )

    def contagem_palavras(self, obj):
        if obj.about:
            qtd = len(obj.about.split())
            preview = obj.about[:100] + ('...' if len(obj.about) > 100 else '')
            return format_html(
                '<div title="{}"><strong>{} palavras</strong><br><small>{}</small></div>',
                obj.about, qtd, preview
            )
        return format_html('<span style="color: #999;">Sem conteúdo</span>')
    contagem_palavras.short_description = 'Conteúdo Sobre'

    def preview_avatar(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;">',
                obj.avatar.url
            )
        return format_html('<span style="color: #999;">Sem avatar</span>')
    preview_avatar.short_description = 'Avatar'

# Admin para grupos de habilidade (skill groups)
class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0
    fields = ('title', 'icon', 'is_active')
    classes = ('collapse',)

@admin.register(SkillGroup)
class SkillGroupAdmin(BaseAdmin):
    list_display = ('title', 'contagem_skills', 'contagem_skills_ativas')
    list_filter = (FilterActive,)
    search_fields = ('title',)
    inlines = [SkillInline]

    def contagem_skills(self, obj):
        total = obj.skill_set.count()
        return format_html('<strong>{}</strong> total', total)
    contagem_skills.short_description = 'Total de Skills'

    def contagem_skills_ativas(self, obj):
        ativ = obj.skill_set.filter(is_active=True).count()
        cor = 'green' if ativ > 0 else 'red'
        return format_html('<span style="color: {};">{} ativas</span>', cor, ativ)
    contagem_skills_ativas.short_description = 'Skills Ativas'

# Admin para Skills
@admin.register(Skill)
class SkillAdmin(BaseAdmin):
    list_display = ('title', 'group', 'preview_icone')
    list_filter = (FilterActive, 'group')
    search_fields = ('title',)
    list_select_related = ('group',)

    fieldsets = (
        ('Detalhes da Skill', {
            'fields': ('title', 'group')
        }),
        ('Visualização', {
            'fields': ('icon',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def preview_icone(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 20px;"></i>', obj.icon)
        return format_html('<span style="color: #999;">Sem ícone</span>')
    preview_icone.short_description = 'Ícone'

# Admin para Projetos
@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    list_display = ('title', 'preview_imagem', 'contagem_skills', 'links_disponiveis', 'ordering_index')
    list_editable = ('ordering_index',)
    list_filter = (FilterActive,)
    search_fields = ('title', 'description')
    filter_horizontal = ('skill',)
    ordering = ('ordering_index',)

    fieldsets = (
        ('Informações do Projeto', {
            'fields': ('title', 'description'),
            'classes': ('wide',)
        }),
        ('Mídia', {
            'fields': ('image',),
            'description': 'Imagem do projeto ou screenshot'
        }),
        ('Links', {
            'fields': ('demo_url', 'source_url'),
            'description': 'Links para demonstração e código fonte'
        }),
        ('Tecnologias', {
            'fields': ('skill',),
            'description': 'Selecione as tecnologias/skills usadas'
        }),
        ('Configurações de exibição', {
            'fields': ('ordering_index', 'is_active'),
            'classes': ('collapse',)
        }),
    )

    def preview_imagem(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;">',
                obj.image.url
            )
        return format_html('<span style="color: #999;">Sem imagem</span>')
    preview_imagem.short_description = 'Prévia'

    def contagem_skills(self, obj):
        count = obj.skill.count()
        return format_html('<span style="background: #e3f2fd; padding: 2px 6px; border-radius: 12px;">{}</span>', count)
    contagem_skills.short_description = 'Skills'

    def links_disponiveis(self, obj):
        links = []
        if obj.demo_url:
            links.append(format_html('<a href="{}" target="_blank" style="color: #1976d2;">Demo</a>', obj.demo_url))
        if obj.source_url:
            links.append(format_html('<a href="{}" target="_blank" style="color: #388e3c;">Código</a>', obj.source_url))
        return format_html(' | '.join(links)) if links else format_html('<span style="color: #999;">Sem links</span>')
    links_disponiveis.short_description = 'Links'

admin.site.register(Sections)
class SectionsAdmin(BaseAdmin):
    list_display = ('about_me', 'projects', 'skills', 'contact')

    fieldsets = (
        ('Informações da Seção', {
            'fields': ('about_me', 'projects', 'skills', 'contact',)
        }),
    )


@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    list_display = ('title', 'description', 'is_active')

    fieldsets = (
        ('Informações de Contato', {
            'fields': ('title', 'description', 'is_active')
        }),
    )

@admin.register(InfoItem)
class InfoItemAdmin(BaseAdmin):
    list_display = ('key', 'value', 'link', 'icon', 'contact', 'is_active')
    list_filter = (FilterActive,)
    search_fields = ('key', 'value')

    fieldsets = (
        ('Detalhes do Item', {
            'fields': ('key', 'value', 'link', 'icon', 'contact'),
            'description': 'Informações adicionais para a seção de contato'
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SocialLink)
class SocialLinkAdmin(BaseAdmin):
    list_display = ('title', 'link', 'icon', 'contact', 'is_active')
    list_filter = (FilterActive,)
    search_fields = ('title', 'link', 'icon', 'contact')

    fieldsets = (
        ('Detalhes do Link', {
            'fields': ('title', 'link', 'icon', 'contact'),
            'description': 'Informações adicionais para a seção de links sociais'
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Footer)
class FooterAdmin(BaseAdmin):
    list_display = ('copyright_text',)
    list_filter = (FilterActive,)
    search_fields = ('copyright_text',)

    fieldsets = (
        ('Informações do Rodapé', {
            'fields': ('copyright_text',)
        }),
    )


@admin.register(Message)
class MessageAdmin(BaseAdmin):
    list_display = ('name', 'email', 'message', 'created')
    list_filter = (FilterActive,)
    search_fields = ('name', 'email', 'message')

    fieldsets = (
        ('Detalhes da Mensagem', {
            'fields': ('name', 'email', 'message',),
            'description': 'Informações sobre a mensagem recebida'
        }),
    )

    def preview_message(self, obj):
        if obj.message:
            texto = obj.message[:50] + ('...' if len(obj.message) > 50 else '')
            return format_html('<span title="{}">{}</span>', obj.message, texto)
        return format_html('<span style="color: #999;">Sem mensagem</span>')
    preview_message.short_description = 'Mensagem'


# Personalização do painel admin
admin.site.site_header = "🎨 Painel de Administração do Portfólio"
admin.site.site_title = "Administração do Portfólio"
admin.site.index_title = "Bem-vindo ao painel de administração do seu portfólio"

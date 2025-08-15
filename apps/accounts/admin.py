from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """

    Administrador Personalizado para o Modelo de Usuário.

    Inherits from:
        BaseUserAdmin: A classe de administração de usuários padrão do aplicativo de autenticação do Django.

    Model:
        User (class): O modelo de usuário personalizado.

    List display:
        - email: Endereço de email do usuário.
        - username: Nome de usuário do usuário.
        - first_name: Primeiro nome do usuário.
        - last_name: Sobrenome do usuário.
        - is_staff: Se o usuário pode acessar o site de administração.
        - is_active: Se o usuário está ativo.

    Fieldsets:
        - None: Campos para email, senha.
        - Informações Pessoais: Campos para nome de usuário, primeiro nome, sobrenome, biografia, site e foto de perfil.
        - Permissões: Campos para status ativo, status de staff, status de superusuário, grupos e permissões de usuário.
        - Datas Importantes: Campos para último login e data de criação da conta.

    Add fieldsets:
        - None: Campos para email, nome de usuário, password1 e password2.

    Search Fields:
        - email: Pesquisar pelo endereço de email do usuário.
        - username: Pesquisar pelo nome de usuário do usuário.

    Ordering:
        - email: Ordenar pelo endereço de email.

    Read-only fields:
        - last_login: A última vez que o usuário fez login.
        - date_joined: A data em que a conta do usuário foi criada.
    """  # noqa: E501

    model = User
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )

    fieldsets = (
        (
            None,
            {"fields": ("email", "password",)},
        ),
        (
            "Informações Pessoais",
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "bio",
                    "website",
                    "profile_picture",
                )
            },
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas Importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email",)
    readonly_fields = (
        "last_login",
        "date_joined",
    )

    def preview_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;">',
                obj.profile_picture.url
            )
        return format_html('<span style="color: #999;">Sem foto de perfil</span>')
    preview_profile_picture.short_description = 'Foto de Perfil'
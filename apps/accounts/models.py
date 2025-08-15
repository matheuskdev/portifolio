from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MinLengthValidator
from django.db import models

from core.utils import regex


class CustomUserManager(BaseUserManager):
    """
    Gerenciador de usuários personalizado.

    Este gerenciador fornece métodos para criar usuários regulares e superusuários.

    Métodos:
        create_user(email, password, **extra_fields):
            Cria e retorna um usuário regular com um email, senha e campos adicionais.

        create_superuser(email, password, **extra_fields):
            Cria e retorna um superusuário com um email, senha e campos adicionais.
    """  # noqa: E501

    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e retorna um usuário regular com um email, senha e campos adicionais.

        Args:
            email (str): O endereço de email do usuário.
            password (str, optional): A senha para o usuário. Padrão é None.
            **extra_fields: Campos adicionais a serem passados para o modelo de usuário.

        Raises:
            ValueError: Se nenhum email for fornecido.

        Returns:
            User: O objeto do usuário criado.
        """  # noqa: E501
        if not email:
            raise ValueError("O campo de email deve ser preenchido.")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria e retorna um superusuário com um email, senha e campos extras.

        Args:
            email (str): O endereço de email do superusuário.
            password (str, optional): A senha para o superusuário. Padrão é None.
            **extra_fields: Campos adicionais a serem passados para o modelo de usuário.

        Returns:
            User: O objeto de superusuário criado.
        """  # noqa: E501
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário personalizado para a aplicação.

    Este modelo estende o AbstractBaseUser e o PermissionsMixin do Django para fornecer
    campos e funcionalidades adicionais, incluindo suporte para email como o
    identificador principal e atributos de usuário personalizáveis.

    Attributes:
        email (EmailField): O endereço de email do usuário, que deve ser único.
        username (CharField): O nome de usuário do usuário, que deve ser único e ter
                              um comprimento mínimo de 4 caracteres.
        first_name (CharField): O primeiro nome do usuário, opcional.
        last_name (CharField): O sobrenome do usuário, opcional.
        bio (TextField): Uma breve biografia do usuário, opcional.
        website (URLField): O site do usuário, opcional.
        profile_picture (ImageField): A foto de perfil do usuário, opcional.
        phone (CharField): O número de telefone do usuário, opcional, validado usando um padrão regex.
        is_active (BooleanField): Indica se a conta do usuário está ativa. O padrão é True.
        is_staff (BooleanField): Indica se o usuário tem permissões de staff. O padrão é False.
        is_superuser (BooleanField): Indica se o usuário é um superusuário. O padrão é False.
        last_login (DateTimeField): A data e hora em que o usuário fez login pela última vez, opcional.
        date_joined (DateTimeField): A data e hora em que o usuário se juntou, definida automaticamente.

    Métodos:
        __str__():
            Retorna o endereço de email do usuário como uma representação em string.

    Meta:
        ordering (list): A ordenação padrão dos usuários pelo email.
        verbose_name (str): O nome singular legível por humanos para o modelo.
        verbose_name_plural (str): O nome plural legível por humanos para o modelo.
        indexes (list): Índice de banco de dados no campo `email` para otimizar consultas.
        constraints (list): Restrições exclusivas para `email` e `username`.

    Custom Manager:
        objects (CustomUserManager): Gerenciador personalizado para criar usuários e superusuários.
    """  # noqa: E501

    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            MinLengthValidator(
                limit_value=4,
                message="O nome de usuário deve ter no mínimo 4 caracteres.",
            )
        ],
    )
    first_name = models.CharField(
        max_length=100, blank=True, verbose_name="Nome"
    )
    last_name = models.CharField(
        max_length=100, blank=True, verbose_name="Sobrenome"
    )
    bio = models.TextField(
        blank=True, null=True, max_length=1012, verbose_name="Biografia"
    )
    website = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
        verbose_name="Foto de Perfil",
    )
    phone = models.CharField(
        max_length=20,
        validators=[regex.phone_regex()],
        help_text="Número de telefone/celular",
        null=True,
        blank=True,
        verbose_name="Telefone",
    )

    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    is_staff = models.BooleanField(default=False, verbose_name="Moderador")
    is_superuser = models.BooleanField(
        default=False, verbose_name="Super Administrador"
    )

    last_login = models.DateTimeField(
        null=True, blank=True, verbose_name="Último Login"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Cadastro"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        """Meta opções para o modelo User."""

        ordering = ["email"]
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        indexes = [
            models.Index(fields=["email"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["email"], name="unique_user_email"
            ),
            models.UniqueConstraint(
                fields=["username"], name="unique_user_username"
            ),
        ]

    def __str__(self):
        """
        Retorna o endereço de email do usuário como uma string.

        Returns:
            str: O endereço de email do usuário.
        """  # noqa: E501
        return self.email
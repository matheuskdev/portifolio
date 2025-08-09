from django.db import models, transaction

class MetaData(models.Model):
    """Armazena metadados para SEO das páginas"""
    title = models.CharField("Título", max_length=255, null=True, blank=True)
    description = models.TextField("Descrição", null=True, blank=True)
    keywords = models.TextField("Palavras-chave", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Metadado"
        verbose_name_plural = "Metadados"
        ordering = ["title"]
        db_table = "metadata"

    def __str__(self):
        return self.title or "Metadado sem título"


class Hero(models.Model):
    """Seção principal do portfólio"""
    greeting = models.CharField(
        "Saudação", max_length=255, default="Olá, meu nome é", null=True, blank=True
    )
    full_name = models.CharField("Nome completo", max_length=255, null=True, blank=True)
    title = models.CharField("Título profissional", max_length=255, null=True, blank=True)
    bio = models.TextField("Biografia", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Hero"
        verbose_name_plural = "Hero"
        ordering = ["full_name"]
        db_table = "hero"

    def save(self, *args, **kwargs):
        """Garante que apenas um Hero esteja ativo por vez"""
        with transaction.atomic():
            if self.is_active:
                Hero.objects.update(is_active=False)
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name or 'Sem nome'} - {self.title or ''}"


class About(models.Model):
    """Seção 'Sobre mim'"""
    about = models.TextField("Descrição", null=True, blank=True)
    avatar = models.ImageField("Foto", upload_to="about/", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sobre"
        verbose_name_plural = "Sobre"
        ordering = ["-id"]
        db_table = "about"

    def save(self, *args, **kwargs):
        """Garante que apenas um About esteja ativo"""
        with transaction.atomic():
            if self.is_active:
                About.objects.update(is_active=False)
            super().save(*args, **kwargs)

    def __str__(self):
        return (self.about[:30] + "...") if self.about else "Sem descrição"


class Project(models.Model):
    """Projetos do portfólio"""
    title = models.CharField("Título", max_length=255, null=True, blank=True)
    description = models.TextField("Descrição", null=True, blank=True)
    image = models.ImageField("Imagem", upload_to="projects/", null=True, blank=True)
    demo_url = models.URLField("URL da demonstração", null=True, blank=True)
    source_url = models.URLField("Código-fonte", default="https://github.com/", null=True, blank=True)
    skill = models.ManyToManyField("Skill", blank=True)
    is_active = models.BooleanField(default=True)
    ordering_index = models.IntegerField("Ordem de exibição", null=True, blank=True)
    created = models.DateTimeField("Data de criação", auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["ordering_index", "-created"]
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        db_table = "projects"

    def __str__(self):
        return self.title or "Projeto sem título"


class SkillGroup(models.Model):
    """Grupo de habilidades"""
    title = models.CharField("Nome do grupo", max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Grupo de habilidades"
        verbose_name_plural = "Grupos de habilidades"
        ordering = ["title"]
        db_table = "skill_groups"

    def __str__(self):
        return self.title or "Grupo sem nome"


class Skill(models.Model):
    """Habilidades individuais"""
    title = models.CharField("Título", max_length=255, null=True, blank=True)
    icon = models.TextField("Ícone (HTML ou classe CSS)", null=True, blank=True)
    group = models.ForeignKey(SkillGroup, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Habilidade"
        verbose_name_plural = "Habilidades"
        ordering = ["title"]
        db_table = "skills"

    def __str__(self):
        return self.title or "Habilidade sem título"


class Contact(models.Model):
    """Informações de contato"""
    title = models.CharField("Título", max_length=255, null=True, blank=True)
    description = models.TextField("Descrição", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        ordering = ["title"]
        db_table = "contacts"

    def __str__(self):
        return self.title or "Contato sem título"


class InfoItem(models.Model):
    """Informações extras de contato (telefone, email, etc.)"""
    key = models.CharField("Chave", max_length=255, null=True, blank=True)
    value = models.TextField("Valor", null=True, blank=True)
    link = models.URLField("Link", null=True, blank=True)
    icon = models.TextField("Ícone", null=True, blank=True)
    contact = models.ForeignKey(Contact, related_name="info_items", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Item de informação"
        verbose_name_plural = "Itens de informação"
        ordering = ["key"]
        db_table = "info_items"

    def __str__(self):
        return self.key or "Item sem chave"


class SocialLink(models.Model):
    """Links de redes sociais"""
    title = models.CharField("Título", max_length=255, null=True, blank=True)
    link = models.URLField("URL", null=True, blank=True)
    icon = models.TextField("Ícone", null=True, blank=True)
    contact = models.ForeignKey(
        Contact,
        related_name="social_links",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Link social"
        verbose_name_plural = "Links sociais"
        ordering = ["title"]
        db_table = "social_links"

    def __str__(self):
        return self.title or "Rede social sem título"


class Sections(models.Model):
    """Controle de visibilidade das seções"""
    about_me = models.BooleanField("Exibir 'Sobre mim'", default=True)
    projects = models.BooleanField("Exibir projetos", default=True)
    skills = models.BooleanField("Exibir habilidades", default=True)
    process = models.BooleanField("Exibir processo", default=True)
    contact = models.BooleanField("Exibir contato", default=True)

    class Meta:
        verbose_name = "Seção"
        verbose_name_plural = "Seções"
        db_table = "sections"

    def __str__(self):
        return "Configuração de seções"


class Message(models.Model):
    """Mensagens enviadas pelo formulário de contato"""
    name = models.CharField("Nome", max_length=255, null=True, blank=True)
    email = models.EmailField("Email", null=True, blank=True)
    message = models.TextField("Mensagem", null=True, blank=True)
    created = models.DateTimeField("Data de envio", auto_now_add=True)

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ["-created"]
        db_table = "messages"

    def __str__(self):
        return self.name or "Mensagem sem nome"


class Footer(models.Model):
    """Informações do rodapé"""
    copyright_text = models.CharField(
        "Texto de copyright",
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Rodapé"
        verbose_name_plural = "Rodapés"
        db_table = "footers"

    def __str__(self):
        return self.copyright_text or "Rodapé sem texto"

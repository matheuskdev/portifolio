from django.core.validators import RegexValidator


def phone_regex():
    """
    Um RegexValidator para validar números de telefone.

    Este validador garante que um número de telefone contenha apenas dígitos
    e tenha entre 9 e 15 caracteres de comprimento. É destinado ao uso
    com campos que capturam números de telefone em modelos ou formulários.

    Attributes:
        regex (str): O padrão de expressão regular usado para validar a entrada.
        message (str): A mensagem de erro exibida quando a entrada não corresponde
                       ao padrão especificado.

    Return:
        Um validador de regex para números de telefone.
    """
    return RegexValidator(
        regex=r"^\d{9,15}$",
        message="Número de telefone deve conter entre 9 e 15 dígitos.",
    )

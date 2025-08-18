from django import template

register = template.Library()

@register.filter(name='add_form_classes')
def add_form_classes(field):
    """
    Adiciona classes do Tailwind a campos de formulário Django.
    """
    default_classes = 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:placeholder-gray-400'
    
    # Aplica as classes apenas se o campo for um widget de input.
    if hasattr(field, 'field'):
        widget_type = field.field.widget.__class__.__name__

        if widget_type in ['TextInput', 'PasswordInput', 'EmailInput', 'NumberInput', 'URLInput', 'Textarea']:
            widget_classes = field.field.widget.attrs.get('class', '')
            new_classes = f'{widget_classes} {default_classes}'.strip()
            field.field.widget.attrs['class'] = new_classes
        elif widget_type == 'RadioSelect':
            field.field.widget.attrs['class'] = 'flex flex-col space-y-2 mt-2'
            return field
    return field
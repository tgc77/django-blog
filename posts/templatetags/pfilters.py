from django import template

register = template.Library()


@register.filter
def plural_comentarios(num_coment: int) -> str:
    if num_coment > 1:
        return f"{num_coment} Comentarios"
    else:
        return f"{num_coment} Comentario"

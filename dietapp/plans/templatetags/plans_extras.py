from django import template

register = template.Library()

@register.simple_tag
def get_range(value):
    """
    Bir sayı verildiğinde 1'den o sayıya kadar olan sayıları döndürür.
    Örnek: 5 verildiğinde [1, 2, 3, 4, 5] döndürür.
    """
    return range(1, int(value) + 1) 
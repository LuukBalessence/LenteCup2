import decimal

from django import template

register = template.Library()


@register.simple_tag
def playing_handicap(hcp, sr, cr, par):
    division_factor = decimal.Decimal(2.0) if par < 40.0 else decimal.Decimal(1.0)
    phcp = int(round((hcp*(sr/113)+(cr-par))/division_factor))
    return phcp
    

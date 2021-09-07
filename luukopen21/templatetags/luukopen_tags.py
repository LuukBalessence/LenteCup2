from django import template

register = template.Library()

@register.simple_tag
def playing_handicap(hcp, sr, cr, par):
    phcp = int(round(hcp*(sr/113)+(cr-par)))
    return phcp
    

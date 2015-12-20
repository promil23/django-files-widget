from django.template import Library
from sorl.thumbnail.templatetags import thumbnail

register = Library()    

def sorl_thumbnail(parser, token):
    return thumbnail(parser, token)

register.tag(sorl_thumbnail)

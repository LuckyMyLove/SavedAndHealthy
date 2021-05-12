from django import template
from django.template.defaultfilters import stringfilter
from googletrans import Translator

register = template.Library()
translator = Translator()

@register.filter
@stringfilter
def translate_text(text):
    pl_text = translator.translate(text, dest='pl')
    return pl_text.text
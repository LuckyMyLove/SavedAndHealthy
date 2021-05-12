from django import template
from googletrans import Translator

register = template.Library()
translator = Translator()

@register.filter
def translate_text(text):
    pl_text = translator.translate(text, dest='pl')
    return pl_text.text
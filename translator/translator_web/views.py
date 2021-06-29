from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.http.request import HttpRequest
from django.utils.safestring import mark_safe

from .translate import get_language_description, translate as _translate
from .translate import get_language_reference


def index(request: HttpRequest):
    return render(request, 'translator_web/index.html')

def translate(request: HttpRequest):
    pseudocode_input = request.GET['translate-text']
    if not pseudocode_input:
        return HttpResponse('')
    try:
        translation = _translate(pseudocode_input, request.GET['translate-language'])
        return HttpResponse(translation)
    except (ValueError, SyntaxError) as e:
        return HttpResponse(str(e))

def specification(request: HttpRequest, language: str):
    context = {}
    if language == 'ru':
        context['message_back'] = 'Назад'
    elif language == 'en':
        context['message_back'] = 'Back'
    else:
        raise Http404

    language_description = get_language_description(language).items()
    language_description_safe = []
    for token, description in language_description:
        language_description_safe.append((token, mark_safe(description)))
    context['language_description'] = language_description_safe
    return render(request, 'translator_web/specification.html', context=context)
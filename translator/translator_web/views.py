from django.http.response import HttpResponse
from django.shortcuts import render
from django.http.request import HttpRequest

from .translate import translate as _translate


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
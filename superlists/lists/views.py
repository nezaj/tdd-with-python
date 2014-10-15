# from django.shortcuts import render
from django.http import HttpResponse

# pylint: disable=unused-argument
def home_page(request):
    return HttpResponse('<html><title>To-Do Lists</title></html>')

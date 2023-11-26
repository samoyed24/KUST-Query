from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from . import forms, models
from .generaltools import get_client_ip
from django.views import generic
from .autoget import querycore
from io import BytesIO
from django.urls import reverse


def index(request):
    IP_address, location = get_client_ip(request)
    log = models.Logging(IP_address = IP_address, location = location, time = timezone.now())
    log.save()
    return render(request, 'index.html')

def menu(request):
    return render(request, 'menu.html')

def login(request, queryType):
    return render(request, 'login.html',
                  {"queryType":queryType})
    
def message(request):
    raise Http404("开发中")

def logs(request):
    raise Http404("开发中")

def get(request):
    username = request.POST['username']
    password = request.POST['password']
    queryType = request.POST['queryType']
    query = querycore.StudentQuery(queryType, username, password)
    query_result = query.do_query()
    if not query_result:
        raise Http404()
    else:
        return query_result
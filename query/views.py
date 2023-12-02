from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from . import forms, models
from .generaltools import get_client_ip, errorMsg
from django.views import generic
from .autoget import querycore
from django.urls import reverse
from .models import Logging, Message
from django.views.decorators.csrf import csrf_exempt


def index(request):
    IP_address, location = get_client_ip(request)
    log = models.Logging(IP_address = IP_address, location = location, time = timezone.now())
    log.save()
    return render(request, 'index.html')

def menu(request):
    return render(request, 'menu.html')

def login(request, queryType):
    selections = {
        'grade':['以网页形式展示', '以xlsx格式返回下载文件'],
        'table':['以xlsx格式返回下载文件'],
        # 'card':['以网页形式展示'],
        'exams':['以网页形式展示', '以xlsx格式返回下载文件'],
        # 'cardBill':['以网页形式展示近15条', '下载xlsx格式开卡以来全部流水', '查看校园卡消费总结']
    }
    return render(request, 'login.html',
                  {"queryType":queryType,
                   "selections":selections[queryType]})
    

class LoggingsListView(generic.ListView):
    model = Logging
    template_name = "logs_view.html"

    def get_queryset(self):
        return Logging.objects.order_by('-time')[:50]

class MessagesListView(generic.ListView):
    model = Message
    template_name = "message.html"

    def get_queryset(self):
        return Message.objects.all()

def get(request):
    username = request.POST['username']
    password = request.POST['password']
    queryType = request.POST['queryType']
    getMode = request.POST['getMode']
    query = querycore.StudentQuery(queryType, username, password, getMode)
    query.do_query()
    return query.result

def leave_message(request):
    username = request.POST['username']
    message = request.POST['message']
    m = Message(username = username, message = message, time = timezone.now())
    m.save()
    return HttpResponse('OK')
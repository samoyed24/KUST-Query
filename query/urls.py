from . import views
from django.urls import path

app_name = 'query'
urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.menu, name="menu"),
    path("<str:queryType>/login", views.login, name="login"),
    path("message", views.message, name="message"),
    path("logs", views.logs, name="logs"),
    path("get", views.get, name="get"),
]

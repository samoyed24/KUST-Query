from . import views
from django.urls import path

app_name = 'query'
urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.menu, name="menu"),
    path("<str:queryType>/login", views.login, name="login"),
    path("logs", views.LoggingsListView.as_view(), name="logs"),
    path("get", views.get, name="get"),
    path('message', views.MessagesListView.as_view(), name="message"),
    path('leave_message', views.leave_message, name="leave_message")
]

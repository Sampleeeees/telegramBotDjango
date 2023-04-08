from django.urls import path

from .views import login_view, base_view

urlpatterns = [
    path("", login_view, name="login"),
    path('base', base_view, name="base")

]

app_name = 'telegrambot'
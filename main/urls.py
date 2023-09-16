from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.button_view, name='main'),
]
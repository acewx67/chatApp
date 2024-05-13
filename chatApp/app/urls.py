from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('',views.index,name='home'),
    path('<str:group_name>/',views.chat,name='chat'),
]
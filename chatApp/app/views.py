from django.shortcuts import render
from .models import Chat,Group
# Create your views here.

def index(request):
    return render(request,'app/user.html')

def chat(request,group_name):
    group = Group.objects.filter(name=group_name).first()
    if group:
        msgs = Chat.objects.filter(group=group)
        return render(request,'app/chat.html',{'group_name':group_name,'msgs':msgs})
    else:
        Group.objects.create(name=group_name)
    return render(request,'app/chat.html',{'group_name':group_name})


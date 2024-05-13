from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'app/user.html')

def chat(request,group_name):
    return render(request,'app/chat.html',{'group_name':group_name})


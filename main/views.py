from django.shortcuts import render
from .insta import getinsta
from .reddit import getreddit
from .telegram import gettelegram
from .youtube import getyoutube
from .facebook import getfbcomments
# from .forms import form1

def start(request):
    return render(request, "start.html", {})

# def info(request):
#     if request.method == 'POST':    
#         user = request.POST.get('username')
#         password = request.POST.get('password')
#         print(user,password)
#         return render(request,"info.html",{'user':user,'pass':password})
#     return render(request, "login.html", {})

# def register(request):
#     # if request.method == 'POST':
#     #     form = form1(request.POST or None)
#     #     if form.is_valid():
#     #         form.save()
#     #     return render(request, "register.html", {})
#     return render(request, "register.html", {})

# def logininsta(request):
#     return render(request,"logininsta.html",{})

# def loginreddit(request):
#     return render(request,"loginreddit.html",{})

def infoinsta(request):
    data=getinsta()
    print(data)
    user=[]
    # com=[]
    for i in data.keys():
        user.append(data[i])
        # com.append(data[i][0][1])
    return render(request,"infoinsta.html",{'user':user})

def inforeddit(request):
    data=getreddit()
    print(data)
    user=[]
    # com=[]
    for i in data:
        user.append([i[0],i[1]])
        # com.append(data[i][0][1])
    print(user,'asdasdasd')
    return render(request,"inforeddit.html",{'user':user})

def infofacebook(request):
    data=getfbcomments()
    return render(request,"infofacebook.html",{'data':data})

def infotelegram(request):
    data=gettelegram()
    print(data)
    user=[]
    # com=[]
    for i in data.keys():
        # temp=[]
        for j in data[i]:
            temp=[]
            temp.append(i)
            temp.append(j)
            user.append(temp)
    print(user)
        # com.append(data[i][0][1])
    return render(request,"infotelegram.html",{'user':user})

def infoyoutube(request):
    data=getyoutube()
    print(data)
    user=[]
    # com=[]
    for i in data.keys():
        user.append(data[i][0])
        # com.append(data[i][0][1])
    return render(request,"infoyoutube.html",{'user':user})


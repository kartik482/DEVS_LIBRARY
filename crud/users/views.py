from multiprocessing import context
from telnetlib import LOGOUT
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login,authenticate,logout
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Skill
from django .contrib import messages
from .forms import customusercreationform,profileForm,skillform,Messageform
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.

def loginpage(request):

    page="login"
    context={"page":page}

    if request.user.is_authenticated:
        return redirect("profiles")




    if request.method=="POST":
        username=request.POST.get("username").lower()
        password=request.POST.get("password")
        print(request.POST)

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"username does not exist")


        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            # messages.success(request,"successfully logged in")
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,"invalid credentials")

    return render(request,"users/login_register.html",context)


def logoutuser(request):
    logout(request)
    messages.success(request,"successfully logged out")
    return redirect("login")


def registeruser(request):
    if request.user.is_authenticated:
        return redirect("account")
    page="register"
    form=customusercreationform()
    if request.method=="POST":
        form=customusercreationform(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,"Registered successfully")

            login(request,user)
            return redirect("editaccount")
        else:
            messages.error(request,"an error has occurred")
            # return redirect("register")


    context={"page":page,"form":form}
    return render(request,"users/login_register.html",context)
    


def profiles(request):
    search_query=''
    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')
    
    skill=Skill.objects.filter(name__icontains=search_query)


    profiles=Profile.objects.distinct().filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query)|Q(skill__in=skill))


    page=request.GET.get('page')
    result=3
    paginator=Paginator(profiles,result)


    try:
        profiles=paginator.page(page)

    except PageNotAnInteger:
        page=1
        profiles=paginator.page(page)

    except EmptyPage:
        page=paginator.num_pages
        profiles=paginator.page(page)



    context={"profiles":profiles,'search_query':search_query,'paginator':paginator}
    return render(request,"users/profiles.html",context)


def userprofiles(request,pk):
    profile=Profile.objects.get(id=pk)
    top_skill=profile.skill_set.exclude(description__exact="")
    other_skill=profile.skill_set.filter(description="")
    context={"profile":profile,"topskill":top_skill,"otherskill":other_skill}
    return render(request,"users/user-profile.html",context)

@login_required(login_url="login")
def useraccount(request):
    profile=request.user.profile
    skill=profile.skill_set.all()
    projects=profile.project_set.all()

    context={"profile":profile,"skill":skill,"projects":projects}
    return render(request,"users/account.html",context)

@login_required(login_url="login") 
def editaccount(request):
    profile=request.user.profile
    form=profileForm(instance=profile)
    if request.method=='POST':
        form=profileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account")


    context={"form":form}
    return render(request,"users/profile-form.html",context)



@login_required(login_url="login") 
def addskill(request):
    profile=request.user.profile
    form=skillform()
    if request.method=='POST':
        form=skillform(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,"skill added successfully")
            return redirect('account')
            
    context={'form':form}
    return render(request,"users/skill-form.html",context)



@login_required(login_url="login") 
def updateskill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    form=skillform(instance=skill)
    if request.method=='POST':
        form=skillform(request.POST,instance=skill)
        
        if form.is_valid():
            form.save()
            messages.success(request,"skill updated successfully")
            return redirect('account')
            
    context={'form':form}
    return render(request,"users/skill-form.html",context)

@login_required(login_url="login") 
def deleteskill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    skill.delete()
    messages.success(request,"skill deleted successfully")
    return redirect('account')


@login_required(login_url="login") 
def inbox(request):
    profile=request.user.profile
    messageRequest=profile.messages.all()
    unreadcount=messageRequest.filter(is_read=False).count()
    context={'messageRequest':messageRequest,'unreadcount':unreadcount}
    return render(request,'users/inbox.html',context)

@login_required(login_url="login") 
def viewmessage(request,pk):
    profile=request.user.profile
    message=profile.messages.get(id=pk)
    if message.is_read==False:
        message.is_read=True
        message.save()
    context={'message':message}
    return render(request,'users/message.html',context)

# @login_required(login_url="login") 
def createmessage(request,pk):
    reciever=Profile.objects.get(id=pk)
    form=Messageform()

    try:
        sender=request.user.profile
    except:
        sender=None

    if request.method=='POST':
        form=Messageform(request.POST)
        message=form.save(commit=False)

        message.sender=sender
        message.reciever=reciever

        if sender:
            message.name=sender.name
            message.email=sender.email
        message.save()
        messages.success(request,"message has been sent successfully")
        return redirect('userprofile',pk=pk)

    context={'reciever':reciever,'form':form}
    return render(request,'users/message_form.html',context)



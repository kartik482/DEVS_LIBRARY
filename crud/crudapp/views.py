from email import message
from multiprocessing import context
import profile
from django.shortcuts import render,HttpResponse,redirect
from . models import Project,Tag
from . forms import ProjectForm,Reviewform
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib import messages

# Create your views here.
def home(request):
    search_query=''
    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')
    
    tags=Tag.objects.filter(name__icontains=search_query)


    projects=Project.objects.distinct().filter(Q(title__icontains=search_query)| Q(description__icontains=search_query) | Q(owner__name__icontains=search_query)|Q(tags__in=tags))



    # projects=Project.objects.all()

    # project.review.all()

#for pagination
    page=request.GET.get('page')
    result=6
    paginator=Paginator(projects,result)


    try:
        projects=paginator.page(page)

    except PageNotAnInteger:
        page=1
        projects=paginator.page(page)

    except EmptyPage:
        page=paginator.num_pages
        projects=paginator.page(page)

    # leftindex=(int(page) - 6)

    # if leftindex < 1:
    #     leftindex = 1
    
    # rightindex=(int(page) + 5)
    # if rightindex > paginator.num_pages:
    #     rightindex= paginator.num_pages + 1


    # custom_range=(1,200)



    # context={"projects":projects,'search_query':search_query,'paginator':paginator,'custom_range':custom_range}
    context={"projects":projects,'search_query':search_query,'paginator':paginator}
    return render(request,"crudapp/home.html",context)


def projectobj(request,pk):
    projectobj=Project.objects.get(id=pk)
    tags=projectobj.tags.all()
    
    form=Reviewform()

    if request.method=='POST':
        profile=request.user.profile
        form=Reviewform(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.project=projectobj
            review.owner=profile
            review.save()
            projectobj.getvotecount
            messages.success(request,'your review has been submitted sucessfully')
            return redirect("project",pk=projectobj.id)
            
        # else:
        #     messages.error(request,'maybe u have already reviewed on this')
        #     return redirect("project")
    context={"projectobj":projectobj,"tags":tags,'form':form}
    return render(request,"crudapp/singleproject.html",context)


@login_required(login_url="login")
def createproject(request):  
    profile=request.user.profile
    form=ProjectForm()

    if request.method=="POST":
        # print(request.POST)
        form=ProjectForm(request.POST,request.FILES)
        print(request.POST)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=profile
            project.save()
            
            return redirect("account")

    context={"form":form}
    return render(request,"crudapp/create-form.html",context)

@login_required(login_url="login")
def updateproject(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    form=ProjectForm(instance=project)

    if request.method=="POST":
        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid:
            form.save()
            return redirect("account")

    context={"form":form}

    return render(request,"crudapp/create-form.html",context)

@login_required(login_url="login")
def deleteproject(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    # project=Project.objects.get(id=pk)
    project.delete()
    return redirect("account")

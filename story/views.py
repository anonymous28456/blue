from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserCreationForm
from django.views.decorators.http import require_http_methods

from .models import Question, Choice, Wish, Genre, Project
#from django.contrib.auth.models import User

from django import forms

def index(request):
    context = {
            "user": request.user
            }
    return render(request, 'story/index.html', context)

def projects(request):
    context = {
            "projects": request.user.project_set.all()
            }
    return render(request, 'story/projects.html',context)

def project_detail(request, project_id):
    project = Project.objects.get(pk=project_id)
    context = {
            "project":project
            }
    return render(request, 'story/project_detail.html', context)

def wishwall(request):
    wishes = Wish.objects.filter(heard_time__isnull=True)

    context = {
            "wishes":wishes,
            }
    return render(request, 'story/wishwall.html', context)
def wish(request):
    if not request.user.is_authenticated:
        return render(request, "story/login.html", {"message": None})
    return render(request, "story/wish.html")

def wishing (request):

    context = {
            "user": request.user,
            "message":"",
            }


    wisher = request.user
    content = request.POST['story']
    genres = request.POST.getlist('genres[]')
    wish_is_invalid=0
    if not genres:
        context["message"]="你沒選創作類型！"
        wish_is_invalid=1

    price = request.POST['price']
    if not price:
        context["message"]+="你沒輸入金錢報酬！"
        wish_is_invalid=1
#    print(wisher,content,genres,price)

    if wish_is_invalid==1:
        print(context)
        return render(request, "story/wish.html", context)
    try:
        wish = Wish.objects.create(
                wisher=wisher,
                content=content,
                price=price
            )
#        print(wish)
        for g in genres:
#            print(g)
            genre = Genre.objects.get(title=g)
            wish.genre.add(genre)
        wish.save()
        return render(request, "story/wish_success.html", context)
    except Exception as e:
        print(e)
        return render(request, "story/wish_fail.html", context)

def wish_detail(request, wish_id):
    wish = Wish.objects.get(pk=wish_id)
    context = {
            "user": request.user,
            "wish": wish
            }
    return render(request, "story/wish_detail.html", context)

def wish_edit(request, wish_id):
    wish = Wish.objects.get(pk=wish_id)
    context = {
            "user": request.user,
            "wish": wish,
            }
    #if art is finished/heard/money received, then cannot edit
    if wish.heard_time is not None:
        context["message"]="藝術家已經接案，無法修改！"
        return render(request, "story/wish_detail.html", context)
    else:
        return render(request, "story/wish_edit.html", context)

def wish_editing(request):
    wish = Wish.objects.get(pk=request.POST['wish_id'])
    content= request.POST['wish_content']
    price = request.POST['wish_price']
    genres = request.POST.getlist('genres[]')
    print(genres)
    if not genres:
        context = {
                "message":"你沒選創作類型！",
                "wish":wish,
                }
        return render(request, "story/wish_edit.html", context)
    try:
        wish.content = content
        wish.price = price
        wish.wish_time = timezone.now()
        wish.genre.clear()

        for g in genres:
            genre = Genre.objects.get(title=g)
            wish.genre.add(genre)
        wish.save()

    except Exception as e:
        context = {
                "message":"更改失敗...請再檢查輸入資料",
                "wish": wish,
                }
        print(e)
        return render(request, "story/wish_edit.html", context)

    context = {
            "wish": wish
            }
    return render(request, "story/wish_detail.html", context)

    
def register(request):
    if request.user.is_authenticated:
        return render(request, "story/user.html")
    return render(request, "story/register.html")


@require_http_methods(["POST"])
def registering(request):
    User = get_user_model()
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        context = {
                "user": user,
                }
        return render(request, 'story/user.html', context)
    else:
        context = {
                "error": True,
                "message": form.errors,
                # TODO: present different message types
                }
        return render(request, 'story/register.html', context)

    
    return HttpResponse(form.errors.as_data())

def login_view(request):
    if not request.user.is_authenticated:
        return render(request, "story/login.html", {"message": None})
    wishes = request.user.wish_made.all().order_by('-wish_time')
    context = {
            "user": request.user,
            "wishes": wishes
            }
    return render(request, 'story/user.html', context)

def logingin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("story:index"))
    else:
        return render(request, "story/login.html", {"message": "INvalid login"})

def logout_view(request):
    logout(request)
    return render(request, "story/index.html", {"message": "Logged out."})

class IndexView(generic.ListView):
    template_name = 'story/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
                pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'story/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'story/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'story/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice!!!!",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('story:results', args=(question.id,)))

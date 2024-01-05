from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

from ASKII import models
from ASKII import forms


# Create your views here.


def index(request):
    questions = models.Question.objects.new_questions()
    page_obj = paginate(questions, request)
    return render(request, template_name="index.html", context={'page_obj': page_obj})


def tag(request, tag_name):
    questions = models.Question.objects.tag_questions(tag_name)
    page_obj = paginate(questions, request)
    return render(request, template_name="tag.html", context={'page_obj': page_obj, 'tg': tag_name})


def question(request, question_id):
    try:
        question = models.Question.objects.get(pk=question_id)
    except models.Question.DoesNotExist:
        return HttpResponse("Запрошенный вопрос не найден", status=404)
    answers = models.Answer.objects.answer_info(question_id)
    page_obj = paginate(answers, request, 5)
    return render(request, template_name="question.html", context={'question': question, 'page_obj': page_obj})


@csrf_protect
def log_in(request):
    if request.method == "GET":
        login_form = forms.LoginForm()
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            print(user)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "Wrong username or password")
    return render(request, "login.html", context={"form": login_form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@csrf_protect
def signup(request):
    if request.method == 'GET':
        user_form = forms.RegisterForm()
    if request.method == 'POST':
        user_form = forms.RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="User saving error")
    return render(request, template_name="signup.html", context={'form': user_form})


@login_required
def settings(request):
    user = request.user
    profile = get_object_or_404(models.Profile, user=user)

    if request.method == 'POST':
        settings_form = forms.SettingsForm(request.POST, request.FILES, instance=profile)
        if settings_form.is_valid():
            settings_form.save(user=user)
            return render(request, template_name="settings.html", context={'form': settings_form})
    else:
        initial_data = {
            'username': user.username,
            'last_name': user.last_name,
            'first_name': user.first_name,
        }
        settings_form = forms.SettingsForm(initial=initial_data, instance=profile)
    return render(request, template_name="settings.html", context={'form': settings_form})


@login_required(login_url='login/', redirect_field_name='continue')
def ask(request):
    if request.method == "POST":
        ask_form = forms.AskForm(request.POST)
        print(ask_form)
        if ask_form.is_valid():
            new_question = ask_form.save(request=request)
            return render(request, template_name="question.html", context={'question': new_question})
        else:
            print("Not valid")
    else:
        print("Not POST")
        ask_form = forms.AskForm()
    return render(request, template_name="ask.html", context={'form': ask_form})


def hot(request):
    questions = models.Question.objects.hot_questions()
    page_obj = paginate(questions, request)
    return render(request, template_name="hot.html", context={'page_obj': page_obj})


def profile(request, profile_id):
    profile = models.Profile.objects.get(pk=profile_id)
    questions = models.Question.objects.profile_questions(profile_id)
    page_obj = paginate(questions, request)
    return render(request, template_name="profile.html", context={'page_obj': page_obj, 'profile': profile})


def paginate(objects, request, per_page=15):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)
    return page_obj


def page_not_found(request, exception):
    return render(request, 'not_existed.html', status=404)

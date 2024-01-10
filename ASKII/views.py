from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import auth, messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

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
    question = models.Question.objects.get(pk=question_id)
    answers = models.Answer.objects.answer_info(question_id)
    page_obj = paginate(answers, request, 5)
    if request.method == "POST":
        answer_form = forms.AnswerForm(request.POST, question=question)
        if answer_form.is_valid():
            answer_form.save(request)
            return redirect(reverse('question', kwargs={'question_id': question_id}) + f'?page={page_obj.paginator.num_pages}')
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
        profile_form = forms.ProfileSettingsForm(request.POST, request.FILES, instance=profile)
        if settings_form.is_valid() and profile_form.is_valid():
            settings_form.save(user=user, request=request)
            profile_form.save(profile=profile)
            messages.success(request, 'Your settings have been successfully updated.')
            return redirect(reverse('settings'))
    else:
        initial_data = {'username': user.username, 'last_name': user.last_name, 'first_name': user.first_name}
        settings_form = forms.SettingsForm(initial=initial_data, instance=profile)
    return render(request, template_name="settings.html", context={'form': settings_form})


@login_required(login_url='login/', redirect_field_name='continue')
def ask(request):
    if request.method == "POST":
        ask_form = forms.AskForm(request.POST)
        if ask_form.is_valid():
            new_question = ask_form.save(request=request)
            return redirect('question', question_id=new_question.id)
    else:
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


@require_POST
@login_required()
def like(request):
    question_id = request.POST['question_id']
    question = models.Question.objects.get(id=question_id)
    author = request.user.profile
    try:
        existing_like = models.QuestionLike.objects.get(question=question, author=author)
        existing_like.delete()
    except models.QuestionLike.DoesNotExist:
        like = models.QuestionLike.objects.create(question=question, author=author)
        like.save()
    return JsonResponse({
        'status': 'ok',
        'likes_count': question.likes.all().count()
    })


@require_POST
@login_required()
def like_answer(request):
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(id=answer_id)
    print(answer_id)
    author = request.user.profile
    try:
        existing_like = models.AnswerLike.objects.get(answer=answer, author=author)
        existing_like.delete()
    except models.AnswerLike.DoesNotExist:
        like = models.AnswerLike.objects.create(answer=answer, author=author)
        like.save()
    return JsonResponse({
        'status': 'ok',
        'likes_count': answer.likes.all().count()
    })


@require_POST
@login_required()
def correct_answer(request):
    if request.method == 'POST':
        answer_id = request.POST.get('answer_id')
        answer = get_object_or_404(models.Answer, id=answer_id)
        if request.user.profile == answer.question.author:
            new_value = not answer.correct
            answer.correct = new_value
            answer.save()
            return JsonResponse({
                'status': 'ok',
                'new_value': new_value
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'You are not authorized to change this answer.'},
                                status=403)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request.'}, status=400)


def paginate(objects, request, per_page=15):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)
    return page_obj


def error_404(request, exception):
    return render(request, 'not_existed.html', {}, status=404)

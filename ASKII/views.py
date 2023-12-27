from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from ASKII import models

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


def ask(request):
    return render(request, template_name="ask.html")


def settings(request):
    return render(request, template_name="settings.html")


def login(request):
    return render(request, template_name="login.html")


def signup(request):
    return render(request, template_name="signup.html")


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

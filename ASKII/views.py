from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'ABOBA ABOBA AAA BBBOOO BBBAAA {i}'
    } for i in range(100)
]

ANSWERS = [
    {
        'id': i,
        'title': f'Answer {i}',
        'content': f'IOUIIOOU UUIOIOIUIOU IOU IOIOIOUUOOI'
    } for i in range(30)
]


# Create your views here.
def index(request):
    page = request.GET.get('page', 1)
    return render(request, template_name="index.html", context={'questions': paginate(QUESTIONS, page)})


def tag(request, tag_name):
    item = tag_name
    page = request.GET.get('page', 1)
    return render(request, template_name="tag.html", context={'tag': item, 'questions': paginate(QUESTIONS, page)})


def question(request, question_id):
    if question_id.isdigit():
        item = QUESTIONS[int(question_id)]
    else:
        item = QUESTIONS[0]
    page = request.GET.get('page', 1)
    return render(request, template_name="question.html", context={'question': item, 'answers': paginate(ANSWERS, page)})


def ask(request):
    return render(request, template_name="ask.html")


def settings(request):
    return render(request, template_name="settings.html")


def login(request):
    return render(request, template_name="login.html")


def signup(request):
    return render(request, template_name="signup.html")


def hot(request):
    page = request.GET.get('page', 1)
    return render(request, template_name="hot.html", context={'questions': paginate(QUESTIONS, page)})


def paginate(objects, page, per_page=15):
    paginator = Paginator(objects, per_page)
    return paginator.page(page)

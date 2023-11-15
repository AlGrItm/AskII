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
    paginator = paginate(QUESTIONS, page)
    page_obj = paginator.get_page(page)
    return render(request, template_name="index.html", context={'page_obj': page_obj})


def tag(request, tag_name):
    item = tag_name
    page = request.GET.get('page', 1)
    paginator = paginate(QUESTIONS, page)
    page_obj = paginator.get_page(page)
    return render(request, template_name="tag.html", context={'tag': item, 'page_obj': page_obj})


def question(request, question_id):
    if question_id.isdigit():
        item = QUESTIONS[int(question_id)]
    else:
        item = QUESTIONS[0]
    page = request.GET.get('page', 1)
    paginator = paginate(ANSWERS, page, 5)
    page_obj = paginator.get_page(page)
    return render(request, template_name="question.html", context={'question': item, 'page_obj': page_obj, 'count': ANSWERS})


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
    paginator = paginate(ANSWERS, page, 5)
    page_obj = paginator.get_page(page)
    return render(request, template_name="hot.html", context={'page_obj': page_obj})


def paginate(objects, page, per_page=15):
    paginator = Paginator(objects, per_page)
    return paginator

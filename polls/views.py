"""
This contains all the views of the polls application
"""
import time
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Question


def home(request):
    """
    Mimic some computation here by sleeping for 0.2 seconds.
    """
    return HttpResponse("ok")


def index(request):
    """
    The index view of polls application.
    It shows the latest 5 questions.
    :param request:
    :return:
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """
    This shows the detail of a particular question.
    :param request:
    :param question_id:
    :return:
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(_, question_id):
    """
    This shows results of a given question.
    :param request:
    :param question_id:
    :return:
    """
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(_, question_id):
    """
    This allows voting on a particular question.
    :param request:
    :param question_id:
    :return:
    """
    message = "You're voting on question"
    return HttpResponse(f"{message} {question_id}.")


@csrf_exempt
def questions(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        now = timezone.now()
        data = {
            'question_text': data['question_text'],
            'pub_date': now,
        }
        question = Question.objects.create(**data)
        response = {
            'id': question.pk
        }
        return HttpResponse(json.dumps(response), content_type='application/json')


def compute(_):
    """
    This mimics a compute intensive application and keeps the CPU occupied for several seconds.
    Added this view to increase CPU load on EC2 instance. We want to test EC2 auto scaling group behaviour.
    """
    for i in range(100000000):
        pass
    return HttpResponse("Ok")


def error(_):
    return HttpResponse("Error", status=500)


def not_found(_):
    return HttpResponse("not found", status=404)

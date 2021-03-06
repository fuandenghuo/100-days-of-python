from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext,loader
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Question,Choice
# Create your views here.



class IndexView(generic.ListView):
    # 指定模板
    template_name = 'polls/index.html'
    # 指定 context 名字
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DeleteView):
    # 指定视图作用的模型
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DeleteView):
    model = Question
    template_name = 'polls/results.html'

def index(request):
    # return HttpResponse("hello,world. You're at the polls index.")

    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = RequestContext(request,{'latest_question_list': latest_question_list})
    # return HttpResponse(template.render)


    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    # return render(request,'polls/index.html',context)
    # res = {"a":"aaaa","b":"bbbb"}
    return HttpResponse(latest_question_list)

def detail(request,question_id):
    # return HttpResponse("you're looking at question %s." % question_id)

    # try:
    #     question = Question.objects.get(pk = question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')
    # return render(request,'polls/detail.html',{'question':question})

    question = get_object_or_404(Question,pk = question_id)
    return render(request,'polls/detail.html',{'question':question})


def result(request,question_id):
    # return HttpResponse("you're looking at result of the question %s." % question_id)
    question = get_object_or_404(Question,pk = question_id)
    return render(request,'polls/results.html',{'question':question})


def vote(request,question_id):
    # return HttpResponse("you're voting on question %s." % question_id)

    p = get_object_or_404(Question,pk = question_id)
    try:
        selected_choice = p.choice_set.get(pk = request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':p,
                                                   'error_message':"you didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 点击提交按钮之后，重定向 url，reversed 视图的名字，视图中需要匹配的参数
        return HttpResponseRedirect(reverse('polls:result',args=(p.id,)))
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView

from app.models import User, Question, Answer, Tag, AnswerLike, QuestionLike


def get_page_range(page, paginator):
    current = page.number
    last = paginator.num_pages

    start_pages = [1, 2, 3]
    end_pages = [last - 2, last - 1, last]

    middle_pages = [
        current - 1,
        current,
        current + 1
    ]

    pages = set()

    for p in start_pages + middle_pages + end_pages:
        if 1 <= p <= last:
            pages.add(p)

    pages = sorted(pages)

    final = []
    for i, p in enumerate(pages):
        final.append(p)

        if i < len(pages) - 1:
            next_p = pages[i+1]
            if next_p - p > 1:
                final.append("...")

    return final


def paginate(objects_list, page_number, per_page=10):
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


class IndexView(TemplateView):
    http_method_names=['get',]
    template_name='app/index.html'
    QUESTIONS_PER_PAGE = 4

    def get_questions(self, tag=None):
        if tag is None:
            return Question.objects.all().order_by('-created_at')

        return Question.objects.filter(tags__title__in=[tag])

    def get_tags(self):
        return Tag.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        tag = self.request.GET.get('tag', None)
        page_number = kwargs.get('page') or int(self.request.GET.get('page', 1))

        questions = self.get_questions(tag)

        paginator = Paginator(questions, self.QUESTIONS_PER_PAGE)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        page_range = get_page_range(page_obj, paginator)

        context['page'] = page_obj
        context['questions_per_page'] = self.QUESTIONS_PER_PAGE
        context['count_questions'] = questions.count()
        context['max_page'] = paginator.num_pages
        context['pages'] = page_range
        context['questions'] = page_obj.object_list
        context['tags'] = self.get_tags()

        return context

    def dispatch(self, request, *args, **kwargs):
        print(request)
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class QuestionView(TemplateView):
    http_method_names = ['get']
    template_name = 'app/question.html'
    ANSWERS_PER_PAGE = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question_id = kwargs.get('question_id')
        page_number = kwargs.get('page') or int(self.request.GET.get('page', 1))

        question = Question.objects.prefetch_related('tags').get(id=question_id)

        answers_list = Answer.objects.filter(question=question).order_by('-created_at')

        paginator = Paginator(answers_list, self.ANSWERS_PER_PAGE)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        page_range = get_page_range(page_obj, paginator)

        context['question'] = question
        context['answers'] = page_obj.object_list
        context['page'] = page_obj
        context['page_range'] = page_range
        context['answers_per_page'] = self.ANSWERS_PER_PAGE
        context['max_page'] = paginator.num_pages

        return context

    def dispatch(self, request, *args, **kwargs):
        print(request)
        return super(QuestionView, self).dispatch(request, *args, **kwargs)


def ask(request):
    return render(request, "ask.html")

def login(request):
    return render(request, "login.html")

def question(request, question_id):


    context = {
        'question': question_data,
        'answers': answers,
    }

    return render(request, "question.html", context)


def settings(request):
    return render(request, "settings.html")

def signup(request):
    return render(request, "signup.html")

def tag(request, tag_name, page):
    questions = []
    for i in range(1, 30):
        questions.append({
            'id': i,
            'title': f'What is Frutiger Aero? {i}',
            'text': 'Guys, tell me more about the aesthetics of the early internet!',
            'votes': 42,
            'count': 3,
            'tags': ['frutiger_aero', '2000s'],
        })

    paginator = Paginator(questions, 5)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    page_range = get_page_range(page_obj, paginator)

    return render(request, "tag.html", {
        'tag_name': tag_name,
        'questions': page_obj.object_list,
        'page': page_obj,
        'page_range': page_range
    })

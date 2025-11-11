from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def index(request, page=1):
    questions = []
    for i in range(1, 3000):
        questions.append({
            'id': i,
            'title': f'What is Frutiger Aero? {i}',
            'text': 'Guys, tell me more about the aesthetics of the early internet!',
            'votes': 42,
            'count': 3,
            'tags': ['frutiger_aero', '2000s'],
        })

    paginator = Paginator(questions, 5)
    page_obj = paginator.get_page(page)

    page_range = get_page_range(page_obj, paginator)

    return render(request, "index.html", {
        "page": page_obj,
        "page_range": page_range,
        "questions": page_obj.object_list
    })

def ask(request):
    return render(request, "ask.html")

def login(request):
    return render(request, "login.html")

from django.shortcuts import render

def question(request, question_id):
    question_data = {
        'id': question_id,
        'title': 'What is Frutiger Aero?',
        'text': """Guys, tell me more about the aesthetics of the early internet!
I've been seeing a lot of content about Frutiger Aero lately,
and I feel intensely nostalgic for the 2000s and early 2010s,
even though I didn't experience them directly.

What are the core visual elements (aqua, glass, gloss, bubbles,
nature elements) and cultural context that gave rise to this
aesthetic? Is it just Windows Vista and Mac OS X, or is there
more to it?""",
        'votes': 42,
        'tags': ['frutiger_aero', '2000s', 'aesthetic'],
        'author': 'AeroLover25',
        'date': '12 Sep 2025',
    }

    answers = [
        {
            'author': 'DesignGuru',
            'date': '14 Sep 2025',
            'votes': 105,
            'text': (
                "Frutiger Aero (FA) is more than just a style; it's a reflection "
                "of early 21st-century optimism about technology and a digital "
                "future that felt clean, shiny, and close to nature. "
                "Core elements include skeuomorphism, high-gloss 'Aqua' interfaces, "
                "realistic bubbles, vibrant blues and greens, and images of sky and water."
            ),
            'is_correct': True
        },
        {
            'author': 'VistaFan',
            'date': '15 Sep 2025',
            'votes': 15,
            'text': (
                "It's strongly associated with Windows Vista's Aero theme, which "
                "used a lot of transparency ('glass') and gradient effects. That, "
                "combined with general optimism after the dot-com bubble burst, "
                "created a unique visual identity."
            ),
            'is_correct': False
        },
        {
            'author': 'AeroEnthusiast',
            'date': '16 Sep 2025',
            'votes': 7,
            'text': "The style often used glossy buttons, glass-like windows, and rounded edges.",
            'is_correct': False
        },
    ]

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

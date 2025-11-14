import typing as t

from django.core.management.base import BaseCommand

from app.models import Question, User


FAKE_QUESTION_DETAILED = """
Guys, tell me more about the aesthetics of the early internet!
I've been seeing a lot of content about Frutiger Aero lately,
and I feel intensely nostalgic for the 2000s and early 2010s,
even though I didn't experience them directly.

What are the core visual elements (aqua, glass, gloss, bubbles,
nature elements) and cultural context that gave rise to this
aesthetic? Is it just Windows Vista and Mac OS X, or is there
more to it?"""

class Command(BaseCommand):
    help = 'Генерация сущностей по модели Вопроса'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=100)

    def get_exist_user(self) -> t.Optional[User]:
        return User.objects.filter(is_superuser=True).first()

    def handle(self, *args, **options):
        count = options.get('count')
        count_exists_questions = Question.objects.all().count()
        questions_to_create = []
        for n in range(count):
            questions_to_create.append(Question(
                title=f"What is Frutiger Aero? #{count_exists_questions + n + 1}",
                detailed=FAKE_QUESTION_DETAILED,
                author=self.get_exist_user()
            ))

        Question.objects.bulk_create(questions_to_create, batch_size=100)
        print("Было создано {} вопрос в БД".format(len(questions_to_create)))

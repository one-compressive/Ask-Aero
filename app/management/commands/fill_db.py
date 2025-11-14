import typing as t
import random

from django.core.management.base import BaseCommand

from app.models import Question, User, Answer, AnswerLike, Tag, QuestionLike


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
    help = 'Генерация тестовых данных'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def get_exist_user(self) -> t.Optional[User]:
        return User.objects.filter(is_superuser=True).first()

    def handle(self, *args, **options):
        ratio = options.get('ratio')

        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_likes = ratio * 200

        print(f"[INFO] Ratio: {ratio}")

        print("[1/5] Создаём пользователей...")

        users_to_create = []
        for i in range(num_users):
            users_to_create.append(
                User(username=f"user_{i+1}", email=f"user_{i+1}@mail.com")
            )
        User.objects.bulk_create(users_to_create, batch_size=500)

        users = list(User.objects.all())
        if len(users) == 0:
            raise Exception("Не найдено пользователей!")


        print("[2/5] Создаём теги...")
        tags_to_create = []
        for i in range(num_tags):
            tags_to_create.append(Tag(title=f"tag_{i+1}"))
        Tag.objects.bulk_create(tags_to_create, batch_size=500)

        tags = list(Tag.objects.all())


        print("[3/5] Создаём вопросы...")
        questions_to_create = []
        for i in range(num_questions):
            questions_to_create.append(
                Question(
                    title=f"Question #{i+1}",
                    text=FAKE_QUESTION_DETAILED,
                    author=random.choice(users),
                )
            )

        Question.objects.bulk_create(questions_to_create, batch_size=500)
        questions = list(Question.objects.all())

        for q in questions:
            q.tags.add(*random.sample(tags, k=min(3, len(tags))))

        print("[4/5] Создаём ответы...")
        answers_to_create = []
        for i in range(num_answers):
            answers_to_create.append(
                Answer(
                    question=random.choice(questions),
                    author=random.choice(users),
                    answer_text="Some answer text..."
                )
            )

        Answer.objects.bulk_create(answers_to_create, batch_size=1000)
        answers = list(Answer.objects.all())


        print("[5/5] Создаём лайки...")

        question_likes = []
        answer_likes = []

        for i in range(num_likes):
            question_likes.append(
                QuestionLike(
                    question=random.choice(questions),
                    user=random.choice(users),
                    value=random.choice([1, -1]),
                )
            )
            answer_likes.append(
                AnswerLike(
                    answer=random.choice(answers),
                    user=random.choice(users),
                    value=random.choice([1, -1]),
                )
            )

        QuestionLike.objects.bulk_create(
            question_likes, batch_size=500, ignore_conflicts=True
        )
        AnswerLike.objects.bulk_create(
            answer_likes, batch_size=500, ignore_conflicts=True
        )

        print("Готово! База успешно заполнена.")

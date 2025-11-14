from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum


class DefaultModel(models.Model):
    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания", editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления", editable=False, null=True)


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Question(DefaultModel):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True, verbose_name="Теги")

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super(Question, self).save(*args, **kwargs)

    @property
    def score(self):
        result = self.likes.aggregate(score=Sum('value'))['score'] or 0
        return result


class Answer(DefaultModel):
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return "Ответ на вопрос ID=" + str(self.question_id)

    @property
    def score(self):
        result = self.likes.aggregate(score=Sum('value'))['score'] or 0
        return result


class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    title = models.CharField(max_length=200, verbose_name="Название тега")

    def __str__(self):
        return self.title


class AnswerLike(models.Model):
    class Meta:
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'
        unique_together=('answer', 'user')

    LIKE = 1
    DISLIKE = -1
    VALUE_CHOICES = [
        (LIKE, 'лайк'),
        (DISLIKE, 'дизлайк'),
    ]

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    value = models.SmallIntegerField(
        choices=VALUE_CHOICES,
        default=LIKE,
        verbose_name="Лайк/дизлайк"
    )

    def __str__(self):
        return f"Был поставлен {dict(self.VALUE_CHOICES).get(self.value)} пользователем {self.user} на ответ {self.answer}"
# HACK: сделать так, чтобы в админке можно было менять лайк на дизлайк

class QuestionLike(models.Model):
    class Meta:
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'
        unique_together=('question', 'user')

    LIKE = 1
    DISLIKE = -1
    VALUE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(
        choices=VALUE_CHOICES,
        default=LIKE,
        verbose_name="Лайк/дизлайк"
    )

    def __str__(self):
        return f"Был поставлен {dict(self.VALUE_CHOICES).get(self.value)} пользователем {self.user}"

from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum, Q
from app.models import Tag, User, Question, Answer, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = 'Update cache for popular tags and best members'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force cache update even if cache exists',
        )

    def handle(self, *args, **options):
        three_months_ago = timezone.now() - timedelta(days=90)
        one_week_ago = timezone.now() - timedelta(days=7)

        popular_tags = Tag.objects.filter(
            question__created_at__gte=three_months_ago,
            question__is_active=True
        ).annotate(
            question_count=Count('question', distinct=True)
        ).order_by('-question_count')[:10]

        tags_data = [
            {
                'id': tag.id,
                'title': tag.title,
                'count': tag.question_count
            }
            for tag in popular_tags
        ]

        cache.set('popular_tags', tags_data, 3600)

        recent_questions = Question.objects.filter(
            created_at__gte=one_week_ago,
            is_active=True
        ).select_related('author')

        recent_answers = Answer.objects.filter(
            created_at__gte=one_week_ago,
            is_active=True
        ).select_related('author')

        user_scores = {}

        for question in recent_questions:
            user_id = question.author_id
            question_score = question.score
            user_scores[user_id] = user_scores.get(user_id, 0) + question_score

        for answer in recent_answers:
            user_id = answer.author_id
            answer_score = answer.score
            user_scores[user_id] = user_scores.get(user_id, 0) + answer_score

        sorted_users = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        user_ids = [user_id for user_id, _ in sorted_users]

        best_members = User.objects.filter(id__in=user_ids).values('id', 'username')
        members_dict = {user['id']: user['username'] for user in best_members}

        best_members_data = [
            {
                'id': user_id,
                'username': members_dict.get(user_id, 'Unknown'),
                'score': score
            }
            for user_id, score in sorted_users if user_id in members_dict
        ]

        cache.set('best_members', best_members_data, 3600)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully cached {len(tags_data)} popular tags and {len(best_members_data)} best members'
            )
        )

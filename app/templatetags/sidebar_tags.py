from django import template
from django.core.cache import cache
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from app.models import Tag, User, Question, Answer

register = template.Library()


@register.inclusion_tag('app/popular_tags.html', takes_context=False)
def popular_tags():
    tags = cache.get('popular_tags')
    if tags is None:
        three_months_ago = timezone.now() - timedelta(days=90)
        popular_tags_qs = Tag.objects.filter(
            question__created_at__gte=three_months_ago,
            question__is_active=True
        ).annotate(
            question_count=Count('question', distinct=True)
        ).order_by('-question_count')[:10]

        tags = [
            {
                'id': tag.id,
                'title': tag.title,
                'count': tag.question_count
            }
            for tag in popular_tags_qs
        ]
        cache.set('popular_tags', tags, 3600)
    return {'tags': tags or []}


@register.inclusion_tag('app/best_members.html', takes_context=False)
def best_members():
    members = cache.get('best_members')
    if members is None:
        one_week_ago = timezone.now() - timedelta(days=7)

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

        best_members_qs = User.objects.filter(id__in=user_ids).values('id', 'username')
        members_dict = {user['id']: user['username'] for user in best_members_qs}

        members = [
            {
                'id': user_id,
                'username': members_dict.get(user_id, 'Unknown'),
                'score': score
            }
            for user_id, score in sorted_users if user_id in members_dict
        ]
        cache.set('best_members', members, 3600)
    return {'members': members or []}

from django.urls import path
from .views import QuestionListView, QuestionView, AuthView, CreateQuestionView, RegisterView, ask, settings, logout_view, QuestionLikeAPI, AnswerLikeAPI, MarkCorrectAnswerAPI, SearchAPI


urlpatterns = [
    path('', QuestionListView.as_view(), name='index'),
    path('page/<int:page>/', QuestionListView.as_view(), name='index_page'),
    path('ask/', CreateQuestionView.as_view(), name='ask'),
    path('login/', AuthView.as_view(), name='login'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('settings/', settings, name='settings'),
    path('question/<int:question_id>/', QuestionView.as_view(), name='question'),
    path('logout/', logout_view, name="logout"),
    path('question/<int:question_id>/like', QuestionLikeAPI.as_view(), name='question_like'),
    path('question/<int:question_id>/dislike', QuestionLikeAPI.as_view(), name='question_dislike'),
    path('answer/<int:answer_id>/like', AnswerLikeAPI.as_view(), name='answer_like'),
    path('answer/<int:answer_id>/dislike', AnswerLikeAPI.as_view(), name='answer_dislike'),
    path('answer/<int:answer_id>/correct/', MarkCorrectAnswerAPI.as_view(), name='mark_correct'),
    path('api/search/', SearchAPI.as_view(), name='search_api'),
]

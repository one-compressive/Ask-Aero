from django.urls import path
from .views import QuestionListView, QuestionView, AuthView, CreateQuestionView, RegisterView, ask, settings, logout_view


urlpatterns = [
    path('', QuestionListView.as_view(), name='index'),
    path('page/<int:page>/', QuestionListView.as_view(), name='index_page'),
    path('ask/', CreateQuestionView.as_view(), name='ask'),
    path('login/', AuthView.as_view(), name='login'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('settings/', settings, name='settings'),
    path('question/<int:question_id>/', QuestionView.as_view(), name='question'),
    path('logout/', logout_view, name="logout"),
]

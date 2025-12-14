from django.urls import path
from .views import QuestionListView, QuestionView, login, ask, signup, settings


urlpatterns = [
    path('', QuestionListView.as_view(), name='index'),
    path('page/<int:page>/', QuestionListView.as_view(), name='index_page'),
    path('ask/', ask, name='ask'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('settings/', settings, name='settings'),
    path('question/<int:question_id>/', QuestionView.as_view(), name='question'),
]

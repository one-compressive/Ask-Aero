from django.urls import path
from .views import QuestionListView, QuestionView, AuthView, ask, signup, settings, logout_view


urlpatterns = [
    path('', QuestionListView.as_view(), name='index'),
    path('page/<int:page>/', QuestionListView.as_view(), name='index_page'),
    path('ask/', ask, name='ask'),
    path('login/', AuthView.as_view(), name='login'),
    path('signup/', signup, name='signup'),
    path('settings/', settings, name='settings'),
    path('question/<int:question_id>/', QuestionView.as_view(), name='question'),
    path('logout/', logout_view, name="logout"),
]

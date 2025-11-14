from django.urls import path
from .views import IndexView, QuestionView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('page/<int:page>/', IndexView.as_view(), name='index_page'),
    #path('ask/', views.ask, name='ask'),
    #path('login/', views.login, name='login'),
    #path('signup/', views.signup, name='signup'),
    #path('settings/', views.settings, name='settings'),
    #path('tag/<str:tag_name>/page/<int:page>/', views.tag, name='tag'),
    path('question/<int:question_id>/', QuestionView.as_view(), name='question'),
]

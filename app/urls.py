from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('page/<int:page>/', views.index, name='index_page'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),
    path('tag/<str:tag_name>/page/<int:page>/', views.tag, name='tag'),
    path('question/<int:question_id>/', views.question, name='question'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('community/', views.community_list, name='community_list'),
    path('community/group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('profile/', views.profile, name='profile'),
    path('join/', views.join, name='join'),
]

from django.urls import path
from blog_write import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import StatistikaView, logout_view


urlpatterns = [
    path("", views.starting_page, name = 'starting-page'),
    path('articles/<slug:slug>', views.full_article, name = 'full_article'),
    path('about/', views.about, name = 'about'),
    path('numra/', views.numra, name = 'numra' ),
    path('statistika/',  StatistikaView.as_view(), name='statistika'),
    path('logout/', logout_view, name='logout')
]


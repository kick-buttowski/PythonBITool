from django.urls import path

from . import views

urlpatterns = [
    path("", views.search_view, name="search_view"),
    path('search/', views.search_view, name='search_view'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('dashboard/<str:dashboard_name>/', views.ind_dashboard_view, name='ind_dashboard_view'),
    path('about/', views.about_view, name='about_view'),
]
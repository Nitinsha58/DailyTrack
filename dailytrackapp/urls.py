from django.urls import path
from . import views

urlpatterns = [
    # DailyTrack app urls.
    path('', views.index, name = 'home'),
    path('delete/<int:pk>/', views.delete, name = 'delete'),
    path('edit/<int:pk>/', views.edit, name = 'edit'),
    path('search/', views.search, name = 'search'),
    path('view/<str:pk>', views.view_data, name = 'view'),

    # login and register urls.
    path("login/", views.loginPage , name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout/", views.logoutUser, name="logout"),
]

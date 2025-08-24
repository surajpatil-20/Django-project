from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('signout/', views.signout_view, name='signout'),
    path('', views.home_view, name='home'),
    path('upload/', views.upload_file, name='upload'),
    path('delete/<int:pk>/', views.delete_file, name='delete_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('about/', views.about, name="about"),
    path("error/", views.error, name="error"),
]

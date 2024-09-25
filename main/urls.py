from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_main, name='redirect_to_main'),
    path('v1/', views.MainViewMain.as_view(), name='main_page'),
]

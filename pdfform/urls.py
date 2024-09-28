from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.FileFormView.as_view(), name='file_form_page'),
    path('filled/', views.file_form_filled, name='file_form_filled'),

    path('remove/expired/', views.remove_expired, name='remove_expired'),
]

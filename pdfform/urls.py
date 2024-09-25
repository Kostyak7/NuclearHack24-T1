from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.PrintFormView.as_view(), name='print_form_page'),
    path('filled/', views.print_form_filled, name='print_form_filled'),

    path('remove/expired/', views.remove_expired, name='remove_expired'),
]

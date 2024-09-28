from django.urls import path
from . import views

urlpatterns = [
    path('<str:fileID>', views.view_result, name='result_page'),
]

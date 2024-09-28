from django.urls import path
from . import views

urlpatterns = [
    path('<str:fileID>', views.wait_result, name='wait_result_page'),
]

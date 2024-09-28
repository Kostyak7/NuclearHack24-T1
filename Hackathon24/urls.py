from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls')),
    path('v1/form/', include('pdfform.urls')),
    path('v1/wait/', include('wait.urls')),
    path('v1/result/', include('result.urls')),
]

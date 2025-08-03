from django.contrib import admin
from django.urls import path
from news.views import NewsList

from django.contrib import admin
from django.urls import path, include

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),  # ← ← ← подключаем маршруты приложения
]
from django.contrib import admin
from youtube_comments import views
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('get-comments/', views.get_comments, name='get_comments'),
]

from django.urls import path, include

urlpatterns = [
    path('test/', include('main.urls.test')),
    path('user/', include('main.urls.user')),
    path('conversation/', include('main.urls.conversation')),
    path('message/', include('main.urls.message')),
]
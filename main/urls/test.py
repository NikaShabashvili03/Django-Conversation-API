# urls.py
from django.urls import path
from main.views.test import TestView

urlpatterns = [
    path('', TestView.as_view(), name='test'),
]



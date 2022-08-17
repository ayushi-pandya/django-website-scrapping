from django.urls import path

from demo.views import DemoFunction

urlpatterns = [
    path('', DemoFunction.as_view(), name='demo_home'),
]

from django.urls import path

from demo import views
from demo.views import DemoFunction

urlpatterns = [
    path('', DemoFunction.as_view(), name='demo_home'),
    # path('home/', Search.as_view(), name='home'),
    path('home/', views.all_search, name='home'),

]

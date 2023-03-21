from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView

# Add your URL paths that belong to the jims_app here
urlpatterns = [
        path(r'', TemplateView.as_view(template_name='home_page.html')),
        path('login/', LoginView.as_view(template_name='login.html'), name='login'),
        path('home_page/', views.home_page, name='home_page'),
        path('accounts/profile/', views.home_page, name='profile'),
]
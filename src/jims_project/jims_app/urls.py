from django.urls import path
from . import views
from django.urls import include, re_path



from django.contrib.auth.views import LoginView

# Add your URL paths that belong to the jims_app here
urlpatterns = [
        path('login/', LoginView.as_view(template_name='login.html'), name='login'),
        path('home_page/', views.home_page, name='home_page'),
        path('accounts/profile/', views.home_page, name='profile'),
        re_path(r'^signup$', views.signup, name='signup'),
]
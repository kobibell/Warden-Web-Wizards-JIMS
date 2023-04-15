from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView

# Add your URL paths that belong to the jims_app here
urlpatterns = [
        path(r'', TemplateView.as_view(template_name='home_page.html')),
        path('login/', LoginView.as_view(template_name='login.html'), name='login'),
        # Need to redirect to home page link
        #path('', views.home_page, name='home_page'),
        path('home_page/', views.home_page, name='home_page'),
        path('accounts/profile/', views.home_page, name='profile'),
        path('accounts/home/', views.accounts_home, name='accounts_home'),
        path('accounts/transactions-details-form/', views.accounts_transaction_details, name='accounts_transaction_details'),
        path('accounts/transactions-details/', views.get_all_transaction_details, name='get_all_transaction_details'),
        path('accounts/search-name/', views.accounts_search_name, name='accounts_search_name'),
        path('accounts/account_list/', views.get_all_accounts, name='get_all_accounts'),
        path('create_user/', views.create_user, name='create_user'),
]
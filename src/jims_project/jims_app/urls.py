from django.urls import path
from . import views
from django.views.generic.base import TemplateView

# Add your URL paths that belong to the jims_app here
urlpatterns = [
        path(r'', views.user_login, name='landing_page'),
        path('login/', views.user_login, name='login'),
        path('home_page/', views.home_page, name='home_page'),
        path('accounts/profile/', views.home_page, name='profile'),
        path('accounts/home/', views.accounts_home, name='accounts_home'),
        path('accounts/transactions-details-form/', views.accounts_transaction_details, name='accounts_transaction_details'),
        path('accounts/transactions-details/', views.get_all_transaction_details, name='get_all_transaction_details'),
        path('accounts/search-name/', views.accounts_search_name, name='accounts_search_name'),
        path('accounts/account_list/', views.get_all_accounts, name='get_all_accounts'),
        path('create_user/', views.create_user, name='create_user'),
        path('create-user/success/', views.create_user_success, name='create_user_success'),
        path('add_inmate', views.add_inmate, name='add_inmate'),
]
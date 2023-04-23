from django.urls import path
from . import views
from django.views.generic.base import TemplateView
from .views import logout_view, logout_success

# Add your URL paths that belong to the jims_app here
# As stated below make sure that the path is using (-)instead of (_)
#!! url paths should use dashes (-) instead of underscores (_)
urlpatterns = [
        #base page for all incoming traffic without url specification
        path(r'', views.user_login, name='login'),

        #basic login page; also acts as landing page for now
        #path('login/', views.user_login, name='login'),

        #home page that will likely be variable for different user types
        path('home-page/', views.home_page, name='home_page'),

        #profile page for modification or viewing account info
        path('accounts/profile/', views.home_page, name='profile'),
        
        #landing page for all cash accounts
        path('accounts/home/', views.accounts_home, name='accounts_home'),

        #form page for transations made for withdrawal or deposits

        path('accounts/transactions-details-form/', views.accounts_transaction_details, name='accounts_transaction_details'),

        #post page for all details retrieved from previous form
        path('accounts/transactions-details/', views.get_all_transaction_details, name='get_all_transaction_details'),

        #search page for cash accounts
        path('accounts/search-name/', views.accounts_search_name, name='accounts_search_name'),

        #!! url paths should use dashes (-) instead of underscores (_)
        #search results page for cash accounts
        path('accounts/account-list/', views.get_all_accounts, name='get_all_accounts'),
        path('accounts/add-money/', views.add_money, name='add_money'),
        path('accounts/withdraw-money/', views.withdraw_money, name='withdraw_money'),

        #user creation page for each of the user types
        path('create-user/', views.create_user, name='create_user'),

        path('create-user/success/', views.create_user_success, name='create_user_success'),

        path('view-inmate/', views.view_inmate, name='view_inmate'),
        path('add_inmate/', views.add_inmate, name='add_inmate'),

        path('view-inmate/inmate-details/', views.get_inmate_details, name='get_inmate_details'),

        path('add-inmate/', views.add_inmate, name='add_inmate'),

        path('home-page/add-inmate/', views.add_inmate, name='add_inmate'),

        path('home-page/inventory/', views.inventory, name='inventory'),

        path('logout/', views.logout_view, name='logout'),

        path('logout-success/', views.logout_success, name='logout_success')

        
]


from django.urls import path , include
from . import views
from django.views.generic.base import TemplateView
from .views import logout_view, logout_success
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# Add your URL paths that belong to the jims_app here
# Make sure that the path is using (-)instead of (_)

urlpatterns = [
        #base page for all incoming traffic without url specification
        path(r'', views.user_login, name='login'),
        
        #!NOTE : DO NOT THINK THIS IS NEEDED ANYMORE (Still under review)
        # path('logout/', views.logout_view, name='logout'),

        path('logout-success/', views.logout_success, name='logout_success'),

        #!NOTE : DO NOT THINK THIS IS NEEDED ANYMORE (Still under review)
        #basic login page; also acts as landing page for now
        #path('login/', views.user_login, name='login'),

        #Home page used for all users
        path('home-page/', views.home_page, name='home_page'),
        
        #landing page for all cash accounts
        path('accounts/home/', views.accounts_home, name='accounts_home'),

        #form page for transations made for withdrawal or deposits
        path('accounts/transactions-details-form/', views.accounts_transaction_details, name='accounts_transaction_details'),

        #post page for all details retrieved from previous form
        path('accounts/transactions-details/', views.get_all_transaction_details, name='get_all_transaction_details'),

        #search page for cash accounts
        path('accounts/search-name/', views.accounts_search_name, name='accounts_search_name'),

        #search results page for cash accounts
        path('accounts/account-list/', views.get_all_accounts, name='get_all_accounts'),
        path('accounts/add-money/', views.add_money, name='add_money'),
        path('accounts/withdraw-money/', views.withdraw_money, name='withdraw_money'),

        # User creation page for any user type
        path('create-user/', views.create_user, name='create_user'),

        #User sucess page for after a user is created
        path('create-user/success/', views.create_user_success, name='create_user_success'),

        # Page for viewing / searching for inmates within the system
        path('view-inmate/', views.view_inmate, name='view_inmate'),

        # Post page for viewing inmates within the system based off search
        path('view-inmate/inmate-details/', views.get_inmate_details, name='get_inmate_details'),

        # Page for adding inmates within the system 
        path('add-inmate/', views.add_inmate, name='add_inmate'),

        # Page for adding an inamtes health sheet when booking an inmate
        path('add-inmate/health-sheet/', views.add_inmate_health_sheet, name='inmate_health_sheet'),
        
        # Page for adding an arrest info when booking an inmate
        path('add-inmate/arrest-information/', views.add_inmate_arrest_information, name='inmate_arrest_info'),

        # Page for adding an gang affiliation when booking an inmate
        path('add-inmate/gang-affiliation/', views.add_inmate_gang_affiliation, name='inmate_gang_affiliation'),

        # Page for adding an vehicle disposition when booking an inmate
        path('add-inmate/vehicle-disposition/', views.add_inmate_vehicle_disposition,name='inmate_vehicle_disposition'),

        # Page for adding an inmates property when booking an inmate
        path('add-inmate/property/', views.add_inmate_property,name='inmate_property'),

        #!NOTE : DO NOT THINK THIS IS NEEDED ANYMORE (Still under review)
        # path('home-page/add-inmate/', views.add_inmate, name='add_inmate'),

        #!TODO : Update / fix to not include 'home-page'. Seems inconsistent with the rest URL patterns.
        
        # Page for viewing the inventory of the JIMS system
        path('home-page/inventory/', views.inventory, name='inventory'),

        # Page for confirming realease of property from inventory
        path('home-page/inventory/update-release-status', views.update_release_status, name='update_release_status'),

        # Page for confirming realease of property from inventory
        path('home-page/inventory/update_release_status_success', views.update_release_status_success, name='success_page'),

        # Page for notifying failure of realease of property from inventory
        path('home-page/inventory/update_release_status_fail', views.update_release_status_fail, name='fail_page'),
]


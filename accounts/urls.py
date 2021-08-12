from django.urls import path
from .views import customers, merchants, auths

app_name = 'accounts'


urlpatterns = [
    # auths urls
    path('signup/', auths.SignUpView.as_view(), name='account-signup'),
    path('signin/', auths.UserLoginView.as_view(), name='account-signin'),
    path('signout/', auths.logout_request, name='account-signout'),

    # account deactivation
    path('deactivate-account/', auths.AccountDeactivateView.as_view(), name='account-deactivate'),

    # password change
    path('password-change/', auths.PasswordChangeView.as_view(), name='password-change'),
    path('password-change/done/', auths.PasswordChangeDoneView.as_view(), name='password-change-done'),

    # password reset
    path('password-reset/', auths.PasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', auths.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset/<uidb64>/<token>/', auths.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password-reset/complete/', auths.PasswordResetCompleteView.as_view(), name='password-reset-complete'),

    # customers urls
    path('customers-signup/', customers.CustomerSignUpView.as_view(), name='customers-signup'),
    path('customer-profile/', customers.CustomerProfileView.as_view(), name='customers-profile'),
    path('customers/', customers.ListCustomersProfileView.as_view(), name='customers-list'),
    path('customer/<str:username>/', customers.ViewCustomerProfileView.as_view(), name='customer-detail'),
    path('customer-confirm-email/<uidb64>/<token>/', customers.AccountActivateView.as_view(),
         name='customer-confirm-email'),

    # merchants urls
    path('merchants-signup/', merchants.MerchantSignUpView.as_view(), name='merchants-signup'),
    path('merchant-profile/', merchants.MerchantProfileView.as_view(), name='merchants-profile'),
    path('merchants/', merchants.ListMerchantsProfileView.as_view(), name='merchants-list'),
    path('merchant/<str:username>/', merchants.ViewMerchantProfileView.as_view(), name='merchant-detail'),
    path('merchant-confirm-email/<uidb64>/<token>/', merchants.AccountActivateView.as_view(),
         name='merchant-confirm-email'),
]

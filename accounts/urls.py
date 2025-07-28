from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('apply-loan/', views.apply_for_loan, name='apply_loan'),
    path('loan-status/', views.loan_status, name='loan_status'),
    path('download-payslip/', views.generate_payslip, name='download_payslip'),
]

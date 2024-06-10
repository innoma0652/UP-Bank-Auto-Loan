from django.urls import path 
from . import views

urlpatterns = [
    path('pay-due/<int:loan_id>/', views.pay_due, name='pay_due'),
    path('create-account',views.account_registration,name="create-account"),
    path('create-account',views.account_registration,name="create-account"),
    path('deposit-money',views.deposit_money,name="deposit-money"),
    path('deposit/approve/<int:deposit_id>/', views.approve_deposit, name='approve_deposit'),
    path('deposit/reject/<int:deposit_id>/', views.reject_deposit, name='reject_deposit'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('my-dues/', views.my_dues, name='my_dues'),
    path('all-dues/', views.all_dues, name='all_dues'),
]


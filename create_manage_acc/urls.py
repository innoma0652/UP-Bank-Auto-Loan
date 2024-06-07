from django.urls import path 
from . import views

urlpatterns = [
    path('create-account',views.account_registration,name="create-account"),
    path('deposit-money',views.deposit_money,name="deposit-money"),
    path('deposit/approve/<int:deposit_id>/', views.approve_deposit, name='approve_deposit'),
    path('deposit/reject/<int:deposit_id>/', views.reject_deposit, name='reject_deposit'),
]


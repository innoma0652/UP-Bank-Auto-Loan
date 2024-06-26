from django.urls import path 
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('review', views.review, name="review"),
    path('approved', views.approved, name="approved"),
    path('rejected', views.rejected, name="rejected"),
    path('',views.logout_page, name="logout"),
    path('view-loan-app/<str:pk>', views.view_loan_app, name="loan-app"),
    path('download-loan-app/<int:pk>', views.GeneratePDF.as_view(), name="generate-pdf"),
    path('approve-loan-app/<int:pk>', views.approve_loan_app, name="approve-loan"),
    path('reject-loan-app/<int:pk>', views.reject_loan_app, name="reject-loan"),
    path('view-deposits/', views.view_deposit_applications, name='view_deposit_applications'),
    path('loaner-status', views.loaner_status, name="loaner-status"),

    path('test', views.test, name="test"),
]
from django.contrib import admin
from django.urls import path, include

from bfl_sdk_app import views

urlpatterns = [
    path('otp/', views.OtpAcceptRequest.as_view()),
    path('auth/', views.AuthAcceptRequest.as_view()),
    path('cancel/', views.CancelAcceptRequest.as_view()),
    path('pod/', views.PodRequestAcceptRequest.as_view()),
    path('eligibility/', views.EligibilityRequestAcceptRequest.as_view()),
    path('requery/', views.ReQueryRequestAcceptRequest.as_view()),
    path('erequery/', views.EnReQueryRequestAcceptRequest.as_view()),
    path('send_request/', views.DataReceive.as_view(), name='send_request'),
]

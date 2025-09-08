from django.urls import path
from . import views

urlpatterns = [
    path('', views.lazypaste_list, name='claims_list'),
    path('search/', views.lazypaste_list, name='claims_search'),
    path('<int:pk>/detail/', views.lazypaste_detail, name='claims_detail'),
    path('<int:pk>/flag/', views.lazypaste_toggle_flag, name='claims_flag'),
    path('<int:pk>/note/', views.lazypaste_add_note, name='claims_add_note'),
    path('<int:pk>/row/', views.lazypaste_row, name='claims_row'),

]

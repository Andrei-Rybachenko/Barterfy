from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_page, name="index"),
    path("ad_list/", views.ads_page, name='ads_list'),
    path("create_ad/", views.create_ad, name='create_ad'),
    path('<int:pk>/edit/', views.edit_ad, name='edit_ad'),
    path('index/', views.index_page, name='index_page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('<int:pk>/delete_ad/', views.delete_ad, name='delete_ad'),
    path('create_proposal/', views.create_proposal, name='create_proposal'),
    path('proposals_list/', views.proposal_page, name='proposals_list'),
    path('<int:pk>/ad_detail/', views.ad_detail, name='ad_detail'),
    path('<int:pk>/proposals/set-status/<str:status>/', views.update_proposal_status, name='update_proposal_status'),

]

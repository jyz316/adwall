from django.urls import path

from . import views

app_name = 'adapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('ads/', views.ads_view, name='ads'),
    path('new_ad/', views.new_ad_view, name='new_ad'),
    path('ad/<int:ad_id>/edit', views.ad_edit, name='edit'),
    path('ad/<int:ad_id>/', views.ad_view, name='ad'),
    path('ad/<int:ad_id>/delete', views.ad_delete, name='delete')



]

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_page, name="register"),
    path('', views.home, name="home"),
    path('trip/<slug:trip_slug>/', views.trip, name="trip"),

    path('profile/<slug:profile_slug>/', views.user_profile, name="user-profile"),
    path('update-user/', views.update_user, name="update-user"),


    path('create-trip/', views.create_trip, name="create-trip"),
    path('update-trip/<slug:trip_slug>', views.update_trip, name="update-trip"),
    path('delete-trip/<slug:trip_slug>', views.delete_trip, name="delete-trip"),

    path('delete-message/<slug:msg_slug>', views.delete_message, name="delete-message"),

    path('types/', views.types_page, name="types"),
    path('activity/', views.activity_page, name="activity")

]

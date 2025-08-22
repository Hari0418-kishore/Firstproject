from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:id>',views.movie_details,name='movie_details'),
    path('movie/<int:movie_id>/showtime/', views.Showtime_and_seats, name='showtime_and_seats'),
    path('get_showtimes/', views.get_showtimes, name='get_showtimes'),
    path('load_seats/', views.load_seats, name='load_seats'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    

    ]
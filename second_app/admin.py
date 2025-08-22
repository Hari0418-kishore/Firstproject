from django.contrib import admin
from .models import movies, Slides, Movie, Showtime, Seat

@admin.register(movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ['title']  # only include fields that exist in the model

@admin.register(Slides)
class SlidesAdmin(admin.ModelAdmin):
    list_display = ['id']  # show primary key or any real field

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title']  # again, only fields that exist

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'date', 'time']
    list_filter = ['movie', 'date']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_number', 'showtime', 'is_booked']
    list_filter = ['showtime', 'is_booked']
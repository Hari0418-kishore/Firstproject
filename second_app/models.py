from django.db import models

# Create your models here.
class movies(models.Model):
    img = models.ImageField(upload_to='pics')
    title = models.CharField(max_length=100)

class Slides(models.Model):
    img = models.ImageField(upload_to= 'img')


class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    description = models.TextField()
    cast = models.TextField()
    trailer = models.URLField()
    poster = models.ImageField(upload_to='posters/')
    backdrop = models.ImageField(upload_to='backdrops/')

    def get_cast_list(self):
        return [name.strip() for name in self.cast.split(',') if name.strip()]

    def youtube_watch_link(self):
        return self.trailer.replace('/embed/', '/watch?v=')

    def __str__(self):
        return self.title
    
class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    date = models.DateField()
    time = models.TimeField()  # Format: HH:MM:SS
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movie.title} - {self.date} {self.time}"

class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat_number} - {self.showtime}"
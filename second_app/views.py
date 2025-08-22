from django.shortcuts import render, get_object_or_404,redirect
from .models import movies,Slides,Movie, Showtime,Seat
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timedelta
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from .models import Showtime, Movie
from datetime import datetime, time as dtime

# Create your views here.
def index(request):
    movie = movies.objects.all()
    slideshow = Slides.objects.all()
    return render (request, "another.html", {'movie': movie ,'slides' : slideshow})
def movie_details(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, 'movie.html', {'movie': movie})

def Showtime_and_seats(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    today = date.today()
    next_5_days = [today + timedelta(days=i) for i in range(5)]
    return render(request, "showtime.html", {
        'movie': movie,
        'next_5_days': next_5_days,
        'is_authenticated': request.user.is_authenticated
    })

# views.py


def get_showtimes(request):
    try:
        movie_id = request.GET.get('movie_id')
        date_str = request.GET.get('date')  # Format: YYYY-MM-DD

        if not movie_id or not date_str:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        showtimes_qs = Showtime.objects.filter(movie_id=movie_id, date=date_obj)

        # Filter out past times if date is today
        now = datetime.now()
        if date_obj == now.date():
            showtimes_qs = showtimes_qs.filter(time__gt=now.time())

        data = {
            'showtimes': [
                {
                    'id': s.id,
                    'time': s.time.strftime('%H:%M')
                } for s in showtimes_qs.order_by('time')
            ]
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='/login/')
def load_seats(request):
    movie_id = request.GET.get('movie_id')
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')
    try:
        showtime = Showtime.objects.get(
            movie_id=movie_id,
            date=date_str,
            time=datetime.strptime(time_str, '%H:%M').time()
        )
        seats = Seat.objects.filter(showtime=showtime)
        booked = [seat.seat_number for seat in seats if seat.is_booked]

        # Generate seat matrix (24 seats per row, 3 sections)
        rows = []
        row_labels = [chr(i) for i in range(ord('A'), ord('H'))]  # A-G (7 rows)
        for row_label in row_labels:
            row_data = []
            for seat_num in range(1, 25):
                seat_id = f"{row_label}{seat_num}"
                row_data.append({
                    'id': seat_id,
                    'booked': seat_id in booked
                })
            rows.append({'label': row_label, 'seats': row_data})

        return render(request, "showtime.html", {
            'rows': rows
        })

    except Showtime.DoesNotExist:
        return render(request, "showtime.html", {'rows': []})

@csrf_exempt
def confirm_booking(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            showtime = Showtime.objects.get(
                movie_id=data['movie_id'],
                date=data['date'],
                time=datetime.strptime(data['time'], '%H:%M').time()
            )
            seats_to_book = data['selected']
            for seat_num in seats_to_book:
                seat, created = Seat.objects.get_or_create(showtime=showtime, seat_number=seat_num)
                seat.is_booked = True
                seat.save()
            return JsonResponse({'status': 'success', 'message': 'Booking successful!'})
        except Showtime.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Showtime not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE")
from models import Movie
import requests


result = []

def quotes():    # 랜덤 영화 인용구 추천
    movies = list(Movie.objects.all())
    for movie in movies:
        id = movie.movie_id
    
        URL = f'https://api.themoviedb.org/3/movie/{id}?api_key=dc9beea6953213907dd536b2b6ef39f6&language=ko-kr'
        movie = requests.get(URL).json()
        if movie.get('tagline') == '':
            result.append(movie)

quotes()
print(result)


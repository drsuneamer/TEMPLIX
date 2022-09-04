# 전체 영화/장르 데이터 json으로 불러오기

# from dotenv import load_dotenv
import requests, json, os


# load_dotenv()
# TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

def get_movies():
    all_movies = []

    for page in range(1, 100):
        URL = f'https://api.themoviedb.org/3/movie/popular?api_key=dc9beea6953213907dd536b2b6ef39f6&language=ko-KR&page={page}'
        movies = requests.get(URL).json()

        for movie in movies['results']:
            if movie.get('release_date', '') and movie.get('poster_path', ''):
                fields = {
                    'movie_id': movie['id'],
                    'title': movie['title'],
                    'release_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'vote_average': movie['vote_average'],
                    'vote_count': movie['vote_count'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'backdrop_path': movie['backdrop_path'],
                    'genres': movie['genre_ids']

                }

                data = {
                    "pk": movie['id'],
                    "model": "movies.movie",
                    "fields": fields,
                }
                    
                all_movies.append(data)

    with open("movie_data.json", "w", encoding="utf-8") as make_json:
        json.dump(all_movies, make_json, indent="\t", ensure_ascii=False)

get_movies()

def get_genres():
    all_genres = []

    URL = f'https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=ko-kr'
    genres = requests.get(URL).json()

    for genre in genres['genres']:
            fields = {
                'genre_id': genre['id'],
                'genre_name': genre['name']

            }
                
            data = {
                    "pk": genre['id'],
                    "model": "movies.genre",
                    "fields": fields,
                }

            all_genres.append(data)

    with open("genre_data.json", "w", encoding="utf-8") as w:
        json.dump(all_genres, w, indent="\t", ensure_ascii=False)

# get_genres()
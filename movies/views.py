from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from dotenv import load_dotenv
from movies.forms import RateForm
from .models import Movie, Rate, Genre
from reviewboard.models import Review
import random, requests, os

load_dotenv()
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

# Create your views here.
def index(request):     # 메인 페이지
    
    if request.user.is_authenticated:
        my_reviews = Review.objects.filter(user_id=request.user.id)
        my_movies = []

        for i in range(len(my_reviews)):
            my_movies.append(Movie.objects.get(pk=my_reviews[i].movie_id))
        
        print_my_movies = my_movies[:12]
    else:
        print_my_movies = []
        
        

    # 1. 현재 인기 영화 순서대로 출력 (상위 15)
    popular_movies = Movie.objects.all().order_by('-vote_count')[:12]

    # 2. 평점 높은 순 (상위 15)
    best_movies = Movie.objects.all().order_by('-vote_average')[:12]

    context = {
        'print_my_movies': print_my_movies,
        'popular_movies': popular_movies,
        'best_movies': best_movies,
    }
    
    return render(request, 'movies/index.html', context)


def all(request):       # 전체 영화 조회 페이지
    movies = Movie.objects.all()

    # 페이지 설정 (한 페이지에 12개씩)
    page = Paginator(movies, 12)
    page_num = request.GET.get('page')
    page_obj = page.get_page(page_num)

    context = {
        'movies': movies,
        'page_obj' : page_obj,
    }
    return render(request, 'movies/all.html', context)


def search(request):    # 영화 제목 기반 검색
    movies = Movie.objects.all()

    searchword = request.GET.get('searchword', '')

    if searchword:
        result_movies = movies.filter(title__contains=searchword)
    else:
        return redirect('movies:all')   # 입력하지 않고 검색 시
        
    context = {
        'result_movies': result_movies,
        }

    return render(request, 'movies/searchresult.html', context)


def detail(request, movie_pk):    # 개별 영화 정보 조회 페이지
    movie = get_object_or_404(Movie, pk=movie_pk)
    genres = movie.genres.all()

    genre = ''

    for g in genres:
        genre += str(g)
        genre += ' / '
    
    genre = genre[:-3]

    

    # 평점 작성
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.movie = movie
            rate.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = RateForm()
        rates = Rate.objects.filter(movie=movie)

        # 전체 평점 평균 구하기
        total = 0
        for r in rates:
            total += r.star
        if total != 0:
            average = round(total / (len(rates)), 1)
        else:
            average = 0

    lock = 'false'
    for rate in rates:
        if request.user == rate.user:
            lock = 'true'

    context = {
        'movie': movie,
        'genre': genre,
        'form': form,
        'rates': rates,
        'average': average,
        'lock': lock,
    }

    return render(request, 'movies/detail.html', context)


@login_required
def like(request, movie_pk):      # 개별 영화 좋아요
    if request.user.is_authenticated:
        user = request.user
        movie = get_object_or_404(Movie, pk=movie_pk)

        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            is_liked = False
        else:
            movie.like_users.add(user)
            is_liked = True
      
        context = {
            'is_liked': is_liked,
            'like_count': movie.like_users.count(),
        }
        return JsonResponse(context)
    return HttpResponse(status=401)


@login_required
def update_rate(request, movie_pk, rate_pk):    # 한줄평 수정
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    rates = Rate.objects.filter(movie=movie)
    rate = get_object_or_404(Rate, pk=rate_pk)

    total = 0
    for r in rates:
        total += r.star
    if total != 0:
        average = round(total / len(rates), 1)
    else:
        average = 0
    if request.user == rate.user:
        if request.method == 'POST':
            form = RateForm(request.POST, instance=rate)
            if form.is_valid():
                rate = form.save(commit=False)
                rate.user = request.user
                rate.save()
                lock = 'true'
                updating = 'false'
                return redirect('movies:detail', movie.pk)
        else:
            form = RateForm(instance=rate)
            lock = 'false'
            updating = 'true'

        context = {
            'form': form,
            'movie': movie,
            'rates': rates,
            'average': average,
            'lock': lock,
            'updating': updating,
        }
        return render(request, 'movies/detail.html', context)
    else:
        return redirect('movies:detail', movie.pk)

    
@login_required
def delete_rate(request, movie_pk, rate_pk):    # 한줄평 삭제
    movie = get_object_or_404(Movie, pk=movie_pk)
    rate = get_object_or_404(Rate, pk=rate_pk)
    if request.user == rate.user and request.method == 'POST':
        rate.delete()
    return redirect('movies:detail', movie.pk)


def cut(request):   # 랜덤 영화 이미지 추천
    # 스틸 이미지가 있는 영화 중에서만 랜덤 1 선택
    movies = list(Movie.objects.filter(backdrop_path__isnull=False))
    movie = random.choice(movies)

    context = {
        'movie': movie,
    }
    
    return render(request, 'movies/cut.html', context)


def quotes(request):    # 랜덤 영화 인용구 추천
    movies = list(Movie.objects.all())
    movie_for_id = random.choice(movies)
    movie_id = movie_for_id.movie_id

    
    URL = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=ko-kr'
    movie = movies = requests.get(URL).json()
    if movie.get('tagline') == '':
        # tagline 없는 영화 조회 시 찾을 때까지 새로 조회
        return redirect('movies:quotes')



    context = {
        'movie': movie,
    }
    
    return render(request, 'movies/quotes.html', context)

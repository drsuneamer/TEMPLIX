from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse,HttpResponse
from reviewboard.models import Review
from movies.models import Movie
from .forms import ReviewForm

# Create your views here.
def index(request):     # 전체 리뷰 조회 인덱스 페이지
    reviews = Review.objects.all().order_by('-pk')  # 최근 작성 게시물이 맨 위에

    context = {
        'reviews': reviews,
    }
    
    return render(request, 'reviewboard/index.html', context)


def detail(request, review_pk):     # 개별 리뷰 조회 페이지
    review = get_object_or_404(Review, pk=review_pk)
    movie = review.movie
    genres = movie.genres.all() 

    genre = ''

    for g in genres:
        genre += str(g)
        genre += ' / '
    
    genre = genre[:-3]



    context = {
        'review': review,
        'genre': genre,
    }
    return render(request, 'reviewboard/detail.html', context)


@login_required
def like(request, review_pk):
    if request.user.is_authenticated:
        user = request.user
        review = get_object_or_404(Review, pk=review_pk)

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            is_liked = False
        else:
            review.like_users.add(user)
            is_liked = True

        context = {
            'is_liked': is_liked, 
            'like_count': review.like_users.count(),
        }
        return JsonResponse(context)
    return HttpResponse(status=401)

@login_required
def create(request):        # 리뷰 작성 페이지
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviewboard:detail', review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'reviewboard/reviewform.html', context)


@login_required
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user or request.user.is_superuser:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('reviewboard:detail', review.pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form
        }
        return render(request, 'reviewboard/reviewform.html', context)
    else:
        return redirect('reviewboard:detail', review.pk)


@login_required
def delete(request, review_pk):
    if request.method == 'POST':
        review = get_object_or_404(Review, pk=review_pk)
        if request.user == review.user or request.user.is_superuser:
            review.delete()
    return redirect('reviewboard:index')
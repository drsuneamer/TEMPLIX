from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('search/', views.search, name='search'),   # 검색 기능 
    path('', views.index, name='index'),    # 메인 페이지
    path('all/', views.all, name='all'),    # 전체 영화
    path('<int:movie_pk>/', views.detail, name='detail'),   # 개별 영화
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/<int:rate_pk>/update/', views.update_rate, name='update_rate'),    # 평가 수정
    path('<int:movie_pk>/<int:rate_pk>/delete/', views.delete_rate, name='delete_rate'),    # 평가 삭제
    
    # 랜덤 영화 추천
    path('pick-your-cut', views.cut, name='cut'),
    path('pick-your-quote', views.quotes, name='quotes'),
]
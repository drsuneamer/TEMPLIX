from django.urls import path
from . import views

app_name = 'reviewboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:review_pk>/update/', views.update, name='update'),
    path('<int:review_pk>/delete/', views.delete, name='delete'),
    path('<int:review_pk>', views.detail, name='detail'),
    path('<int:review_pk>/like/', views.like, name='like'),
]
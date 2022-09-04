from django.contrib import admin
from .models import Movie, Genre

class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title']

# Register your models here.
admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
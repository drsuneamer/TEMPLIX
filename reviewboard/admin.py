from django.contrib import admin
from .models import Review

class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title']

# Register your models here.
admin.site.register(Review)
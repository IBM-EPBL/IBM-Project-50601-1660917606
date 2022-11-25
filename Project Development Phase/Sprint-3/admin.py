from django.contrib import admin

# Register your models here.
from .models import Customer, Article, SavedArticle

admin.site.register(Customer)
admin.site.register(Article)
admin.site.register(SavedArticle)


from django.contrib import admin

from app.articles.models import Article, Category, Rating

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Rating)

from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Article


@register(Article)
class ArticleIndex(AlgoliaIndex):
    fields = [
        "id",
        "author",
        "category",
        "title",
        "description",
        "created_at",
        "updated_at",
    ]

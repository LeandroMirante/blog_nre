from __future__ import absolute_import, unicode_literals
from app.articles.models import Article,Rating
from app.users.models import User
from app.articles.serializers import RatingSerializer
from celery import shared_task

@shared_task()
def count_views(pk):
    pk = int(pk)
    obj = Article.objects.get(pk=pk)
    obj.view_count = obj.view_count + 1
    obj.save(update_fields=("view_count",))

@shared_task()
def rate_article(user_id, article_id, value):
    Rating.objects.create(
            user=User.objects.get(pk=user_id), 
            article=Article.objects.get(pk=article_id), 
            value=value
            )
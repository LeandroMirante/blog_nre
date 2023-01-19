from rest_framework import serializers
from django.db.models import Avg
from .models import Article, Rating, Category


class ArticleSerializerCreate(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "category",
            "author",
            "title",
            "description",
            "file",
            "created_at",
            "updated_at",
        ]

    def get_author(self, obj):
        return obj.author.name


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    # url = serializers.HyperlinkedIdentityField(
    #         view_name='article-detail',
    #         lookup_field='pk'
    # )
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    objectID = serializers.SerializerMethodField()
    num_of_ratings = serializers.SerializerMethodField()
    created_at_timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "objectID",
            "author",
            "category",
            "title",
            "description",
            "file",
            "created_at",
            "updated_at",
            "num_of_ratings",
            "average_rating",
            "created_at_timestamp",
            "view_count",
        ]

    def get_author(self, obj):
        return obj.author.name

    def get_objectID(self, obj):
        return obj.pk

    def get_category(self, obj):
        if obj.category is not None:
            return obj.category.name
        return None

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%d-%m-%Y %H:%M:%S")

    def get_average_rating(self, obj):
        avg = Rating.objects.filter(article_id=obj.pk).aggregate(Avg("value"))[
            "value__avg"
        ]
        if avg is None:
            return "This article do not have any rating"
        else:
            return avg

    def get_num_of_ratings(self, obj):
        return len(Rating.objects.filter(article_id=obj.pk))

    def get_created_at_timestamp(self, obj):
        return obj.created_at.timestamp()


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Rating
        fields = ("value", "user")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)

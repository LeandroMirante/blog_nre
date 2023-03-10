from algoliasearch_django import algolia_engine
from app.articles.serializers import ArticleSerializer
from app.articles.models import Article, Category


def get_client():
    return algolia_engine.client


def get_index(index_name="Article", classify=None, category=None):
    client = get_client()
    index = client.init_index(index_name)
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)

    if classify == "most_recent":
        index.set_settings({"ranking": ["desc(created_at_timestamp)"]})
    if classify == "top_rated":
        index.set_settings({"ranking": ["desc(num_of_ratings)"]})
    if classify == "older":
        index.set_settings({"ranking": ["asc(created_at_timestamp)"]})
    if classify == "best_rated":
        index.set_settings({"ranking": ["desc(average_rating)"]})
    if classify == "most_views":
        index.set_settings({"ranking": ["desc(view_count)"]})
    index.set_settings({'attributesToHighlight':[]})
    index.save_objects(serializer.data)
    return index


def perform_search(query, classify=None, category=None, **kwargs):
    index = get_index("Article", classify, category)
    if category:
        results = index.search(query, {
            'filters': f'category_id = {category}',
            'hitsPerPage': 10
        })
    else:
        results = index.search(query)
    return results

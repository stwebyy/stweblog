from rest_framework import serializers

from .models import Article, Tag, Category




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name')


class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Article
        fields = ('id','created_at', 'title', 'discript', 'text', 'category')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name')

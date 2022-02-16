from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import Post, LikedList, LikedItem


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description']


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedItem
        fields = ['liked_list', 'post']

    def create(self, validated_data):
        liked_list = validated_data.get('liked_list')
        post = validated_data.get('post')

        liked_item, created = LikedItem.objects.get_or_create(post=post, liked_list=liked_list)
        liked_item.is_liked = True
        liked_item.save()

        return liked_item


class UnLikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedItem
        fields = ['liked_list', 'post']

    def create(self, validated_data):
        liked_list = validated_data.get('liked_list')
        post = validated_data.get('post')

        try:
            liked_item = LikedItem.objects.get(post=post, liked_list=liked_list)
        except:
            raise ObjectDoesNotExist

        liked_item.is_liked = False
        liked_item.save()

        return liked_item

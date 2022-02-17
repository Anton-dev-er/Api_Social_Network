import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import Post, LikedItem


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description']


class CountLikedPost(serializers.Serializer):
    date_to = serializers.CharField(max_length=255, write_only=True)
    date_from = serializers.CharField(max_length=255, write_only=True)
    analytics = serializers.DictField(read_only=True)

    def validate(self, data):
        date_to = data.get('date_to')
        date_from = data.get('date_from')

        if not date_from or not date_to:
            raise serializers.ValidationError({'Wrond param': f'[date_from] and [date_to] is required'})

        try:
            valid_date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
            valid_date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')
        except ValueError:
            raise serializers.ValidationError({'Invalid date': 'Should be %Y-%m-%d'})

        db_data = LikedItem.objects.filter(updated__gte=date_from, updated__lt=date_to, is_liked=True)

        count_days = (valid_date_to - valid_date_from).days
        range_dates = [valid_date_from + datetime.timedelta(days=day) for day in range(0, count_days)]

        range_dates_to_dict = {str(key).split(" ")[0]: 0 for key in range_dates}

        for i in db_data:
            date = str(i.updated)
            if date in range_dates_to_dict:
                range_dates_to_dict[f"{date}"] += 1

        data["analytics"] = range_dates_to_dict
        return data


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

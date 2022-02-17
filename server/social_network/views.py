from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import PostSerializer, LikePostSerializer, UnLikePostSerializer, CountLikedPost


class PostView(APIView):
    serializer_class = PostSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikePostView(APIView):
    serializer_class = LikePostSerializer

    def post(self, request):
        liked_list = request.data.get('liked_list')
        post = request.data.get('post')
        data = {
            'liked_list': liked_list,
            'post': post,
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UnLikePostView(APIView):
    serializer_class = UnLikePostSerializer

    def post(self, request):
        liked_list = request.data.get('liked_list')
        post = request.data.get('post')
        data = {
            'liked_list': liked_list,
            'post': post,
        }
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CountLikedPostsView(APIView):
    serializer_class = CountLikedPost

    def get(self, request):
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        data = {
            "date_from": date_from,
            "date_to": date_to
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)






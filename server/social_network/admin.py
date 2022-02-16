from django.contrib import admin

from server.social_network.models import Post, LikedList, LikedItem

admin.site.register(Post)
admin.site.register(LikedList)
admin.site.register(LikedItem)

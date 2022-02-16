from django.contrib import admin

from server.social_network.models import Post, Liked, LikedItem

admin.site.register(Post)
admin.site.register(Liked)
admin.site.register(LikedItem)

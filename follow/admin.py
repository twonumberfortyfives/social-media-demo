from django.contrib import admin

from follow.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass

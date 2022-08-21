from django.contrib import admin

from .models import Farm, Review


class FarmAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'url',
        'reviews_overall',
        'resource',
        'rating'
    )
    list_filter = ('name', 'rating')


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'farm',
        'author',
        'comment',
        'stars',
        'date',
    )

    search_fields = ('comment',)
    list_filter = ('stars', 'date')


admin.site.register(Farm, FarmAdmin)
admin.site.register(Review, ReviewAdmin)

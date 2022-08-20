from django.contrib import admin

from .models import Farm, Review


class FarmAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'url',
        'reviews_overall',
    )
    list_filter = ("name",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'farm',
        'author',
        'comment',
        'stars',
        'date',
        'resource'
    )

    search_fields = ('comment',)
    list_filter = ('stars', 'date', 'resource')


admin.site.register(Farm, FarmAdmin)
admin.site.register(Review, ReviewAdmin)

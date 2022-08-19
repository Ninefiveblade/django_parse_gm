from django.contrib import admin

from .models import Farm, Review


class FarmAdmin(admin.ModelAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Farm, FarmAdmin)
admin.site.register(Review, ReviewAdmin)

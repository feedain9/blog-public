from django.contrib import admin
from . import models

# Register your models here.
class AnalyticsAdmin(admin.ModelAdmin):
    readonly_fields = ('pub_time',)

admin.site.register(models.Article)
admin.site.register(models.Marketing)
admin.site.register(models.Contact)
admin.site.register(models.Newsletter)
admin.site.register(models.Keywords)
admin.site.register(models.ArticleAnalytics)
admin.site.register(models.Analytics, AnalyticsAdmin)
admin.site.register(models.UrlToIndex)
admin.site.register(models.NewsletterTracking)
admin.site.register(models.Comment)
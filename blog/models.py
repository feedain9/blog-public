from django.db import models
from django.utils import timezone

# Create your models here.

class Article(models.Model):
    article_id = models.CharField(default="", max_length=255)
    image = models.TextField(null=True, blank=True)
    image_upload = models.FileField(upload_to='articles/', null=True, blank=True)
    pub_time = models.DateTimeField(auto_now_add=True, editable=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    is_delete = models.BooleanField(default=False)
    extra_data = models.JSONField(default={}, null=True, blank=True)
    read = models.IntegerField(default=0)
    video = models.TextField(default="", null=True, blank=True)
    slug = models.CharField(max_length=255, default="")
    # French
    category = models.CharField(default="Actualites", max_length=255)
    title = models.CharField(max_length=500)
    content = models.TextField()
    content_without_markdown = models.TextField(default="")
    # English
    category_en = models.CharField(default="News", max_length=255)
    title_en = models.CharField(default="", blank=True, null=True, max_length=500)
    content_en = models.TextField(default="", blank=True, null=True)
    # Spanish
    category_es = models.CharField(default="Noticias", max_length=255)
    title_es = models.CharField(default="", blank=True, null=True, max_length=500)
    content_es = models.TextField(default="", blank=True, null=True)
    # German
    category_de = models.CharField(default="Nachrichten", max_length=255)
    title_de = models.CharField(default="", blank=True, null=True, max_length=500)
    content_de = models.TextField(default="", blank=True, null=True)
    # Italian
    category_it = models.CharField(default="Notizie", max_length=255)
    title_it = models.CharField(default="", blank=True, null=True, max_length=500)
    content_it = models.TextField(default="", blank=True, null=True)
    # Korean
    category_ko = models.CharField(default="뉴스", max_length=255)
    title_ko = models.CharField(default="", blank=True, null=True, max_length=500)
    content_ko = models.TextField(default="", blank=True, null=True)
    # Japanese
    category_ja = models.CharField(default="ニュース", max_length=255)
    title_ja = models.CharField(default="", blank=True, null=True, max_length=500)
    content_ja = models.TextField(default="", blank=True, null=True)

    def __str__(self):
        return self.title

class Keywords(models.Model):
    keyword = models.CharField(max_length=255)
    def __str__(self):
        return self.keyword
class Marketing(models.Model):
    asin = models.CharField(default="", max_length=255)
    title = models.CharField(default="", max_length=255)
    image = models.CharField(default="", max_length=255)
    description = models.TextField(default="")
    container = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True, editable=True)
    def __str__(self):
        return self.title

class Contact(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    message = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True, editable=True)
    def __str__(self):
        return self.email

class NewsletterTracking(models.Model):
    subject = models.CharField(max_length=255)
    emails = models.JSONField(default=[], null=True, blank=True)
    date = models.DateField(default=timezone.now().date())
    count = models.IntegerField(default=0)
    def __str__(self):
        return str(self.subject)

class Newsletter(models.Model):
    email = models.EmailField()
    pub_time = models.DateTimeField(auto_now_add=True, editable=True)
    def __str__(self):
        return self.email

class Analytics(models.Model):
    ip = models.CharField(max_length=255)
    ua = models.CharField(max_length=255)
    referer = models.CharField(max_length=255)
    number = models.IntegerField(default=0)
    utm_source = models.CharField(default="", max_length=255)
    url = models.URLField(default="")
    pub_time = models.DateTimeField(auto_now_add=True, editable=True)
    def __str__(self):
        return self.ip

class ArticleAnalytics(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip = models.CharField(max_length=255)
    ua = models.CharField(max_length=255)
    referer = models.CharField(max_length=255)
    number = models.IntegerField(default=0)
    url = models.URLField(default="")
    pub_time = models.DateTimeField(auto_now_add=True, editable=True)
    def __str__(self):
        return self.article.title
    

class UrlToIndex(models.Model):
    url = models.URLField()
    type_index = models.CharField(max_length=255)
    notify_time = models.CharField(max_length=255)
    def __str__(self):
        return self.url
    
class Comment(models.Model):
    article_pk = models.IntegerField(null=True, blank=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    in_reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    pub_time = models.DateTimeField(auto_now_add=True, editable=True)
    disabled = models.BooleanField(default=True)
    def __str__(self):
        return self.message
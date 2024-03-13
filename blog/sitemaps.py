from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from . import models
from django.template.defaultfilters import slugify

class ArticleSitemap(Sitemap):
    protocol = 'https'
    limit = 5000
    def items(self):
        # Retourne une liste des objets de votre modèle à inclure dans le sitemap
        return models.Article.objects.only('pk', 'title').order_by('-pub_time')

    def location(self, item):
        # Retourne l'URL du détail de chaque objet de votre modèle
        return reverse('article_slug', args=[slugify(f"{item.title[:120]}-{item.pk}")])
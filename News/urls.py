"""
URL configuration for News project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog import views, sitemaps
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps import views as sitemaps_view

sitemaps = {
    'articles': sitemaps.ArticleSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('set-lang/<str:language>', views.set_language),
    path('', views.homepage),
    path('mail', views.mail, name="mail"),
    path('<str:language>/search/', views.SearchResults),
    path('search/', views.SearchResults),
    path('<str:language>/', views.homepage),
    path('sitemap.xml', sitemaps_view.index, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemaps_view.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('articles', views.magazine),
    path('<str:language>/articles', views.magazine),
    path('category/', views.category_move),
    path('category/<str:category>', views.category),
    path('<str:language>/category/<str:category>', views.category),
    path('kpop', views.kpop),
    path('<str:language>/kpop', views.kpop),
    path('kdrama', views.kdrama),
    path('<str:language>/kdrama', views.kdrama),
    path('guide', views.guide),
    path('<str:language>/guide', views.guide),
    path('faqs', views.faqs),
    path('<str:language>/faqs', views.faqs),
    path('articles/<str:slug>', views.blog_detail, name="article_slug"),
    path('<str:language>/articles/<str:slug>', views.blog_detail),
    path('redirect', views.redirect_url, name="redirect_url"),
    path('<str:language>/contact', views.contact),
    path('contact', views.contact),
    path('mentions-legales', views.mentionslegales),
    path('cookies/accept/', views.cookies_accept, name="cookies_accept"),
    path("stats", views.adminstats, name="adminstats"),
    path("newsletter", views.newsletter, name="newsletter"),
    path('robots.txt',TemplateView.as_view(template_name="webpage/robots.txt", content_type="text/plain")),
    path('ads.txt',TemplateView.as_view(template_name="webpage/ads.txt", content_type="text/plain")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'blog.views.error_500'
handler404 = 'blog.views.error_404'
import ast
from bs4 import BeautifulSoup
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone, translation
from django.core.paginator import Paginator
import requests
from . import models
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import stringfilter
from django.template.defaultfilters import slugify
from django.template.defaulttags import register as reg
import re
import markdown as mark
from .context_processors import primary_colors_dict
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

md = mark.Markdown()

languages = ["fr", "en", "es", "de", "it", "ko", "ja"]

# Create your views here.

def markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))

    return text


@reg.filter
def create_slug(pk):
    article = models.Article.objects.get(pk=pk)
    slug = slugify(f"{article.title[:120]}-{article.pk}")
    return slug

@reg.filter
def tolist(prelist):
    return ast.literal_eval(prelist)

@reg.filter
@stringfilter
def markdown(value):
    value = re.sub(r"\[(.+)\]\(.+\)", r"\1", value)
    value = md.convert(source=value)
    value = re.sub(r'\n', '  <br>', value)
    return value

@reg.filter
@stringfilter
def clean_markdown(value):
    return markdown_to_text(value)

def error_404(request, exception):
    return render(request, "webpage/404.html", status=404)

def error_500(request):
    return render(request, "webpage/500.html", status=500)

def set_language(request, language):
    if request.method == "GET" and language in languages:
        referer = request.META.get('HTTP_REFERER')
        if language == "fr":
            if referer and ("/en/" in referer or "/es/" in referer or "/de/" in referer or "/it/" in referer or "/ja/" in referer or "/ko/" in referer):
                new_referer = referer.replace("/en/", "/").replace("/es/", "/").replace("/de/", "/").replace("/it/", "/").replace("/ja/", "/").replace("/ko/", "/")
                response = redirect(new_referer)
            elif referer:    
                response = redirect(f"{referer.replace('https://kpopalerts.fr/', f'https://kpopalerts.fr/{language}/')}")
            else:
                return redirect("/")
        else:
            if referer and ("/en/" in referer or "/es/" in referer or "/de/" in referer or "/it/" in referer or "/ja/" in referer or "/ko/" in referer):
                new_referer = referer.replace("/en/", f"/{language}/").replace("/es/", f"/{language}/").replace("/de/", f"/{language}/").replace("/it/", f"/{language}/").replace("/ja/", f"/{language}/").replace("/ko/", f"/{language}/")
                response = redirect(new_referer)
            elif referer:
                response = redirect(f"{referer.replace('https://kpopalerts.fr/', f'https://kpopalerts.fr/{language}/')}")
            else:
                response = redirect(f"/{language}/")
        response.set_cookie('language_code', language, max_age=31536000)
        return response
    return HttpResponseForbidden()


def homepage(request, language="fr"):
    if request.method == "GET" and language in languages:
        translation.activate(language)
        # Restaurez la langue dans la requête (pour la prise en compte immédiate dans la vue actuelle)
        request.LANGUAGE_CODE = translation.get_language()

        article_exclude = []
        article_principal = models.Article.objects.order_by("-pk").first()
        article_exclude.append(article_principal.pk)
        last_2_articles = models.Article.objects.exclude(pk__in=article_exclude).order_by("-pk")[:2]
        for article in last_2_articles:
            article_exclude.append(article.pk)
        last_3_articles = models.Article.objects.exclude(pk__in=article_exclude).order_by("-pk")[:3]
        for article in last_3_articles:
            article_exclude.append(article.pk)
        last_articles = models.Article.objects.exclude(pk__in=article_exclude).order_by("-pk")[:15]

        context = {
            "last_2_articles": last_2_articles,
            "last_3_articles": last_3_articles,
            "article_principal": article_principal,
            "last_articles":last_articles,
            "language":language
        }
        return render(request, "webpage/homepage.html", context)
    return HttpResponseForbidden()


def magazine(request, language="fr"):
    if request.method == "GET" and language in languages:
        translation.activate(language)
        # Restaurez la langue dans la requête (pour la prise en compte immédiate dans la vue actuelle)
        request.LANGUAGE_CODE = translation.get_language()

        all_articles = models.Article.objects.all().order_by("-pub_time")
        paginator = Paginator(all_articles, 25)
        page_number = request.GET.get("page")
        if page_number == "1":
            if language == "fr":
                return redirect("/articles", permanent=True)
            else:
                return redirect(f"/{language}/articles", permanent=True)
        page_obj = paginator.get_page(page_number)
        category = ""
        context = {
            "category_articles": page_obj,
            "category":category,
            "language":language,
        }
        return render(request, "webpage/articles.html", context)
    return HttpResponseForbidden()


def mail(request):
    if request.method == "GET":
        user_agent = request.META.get('HTTP_USER_AGENT', "")
        to_email = request.GET.get("to")
        pk_tracking = request.GET.get("campaign")
        if to_email and pk_tracking and "http://mail.google.com/" not in user_agent:
            if models.NewsletterTracking.objects.filter(pk=pk_tracking).exists():
                tracking = models.NewsletterTracking.objects.get(pk=pk_tracking)
                if to_email not in tracking.emails:
                    tracking.emails.append(to_email)
                    tracking.count += 1
                    tracking.save()
                else:
                    tracking.count += 1
                    tracking.save()
        return redirect(f"https://{primary_colors_dict.get('domain')}/", permanent=True)

def kpop(request, language="fr"):
    if request.method == "GET" and language in languages:
        translation.activate(language)
        # Restaurez la langue dans la requête (pour la prise en compte immédiate dans la vue actuelle)
        request.LANGUAGE_CODE = translation.get_language()

        all_articles = models.Article.objects.all().exclude(Q(category="cinéma") | Q(category="Drama")).order_by("-pub_time")
        paginator = Paginator(all_articles, 25)
        page_number = request.GET.get("page")
        if page_number == "1":
            if language == "fr":
                return redirect("/kpop", permanent=True)
            else:
                return redirect(f"/{language}/kpop", permanent=True)
        page_obj = paginator.get_page(page_number)
        category = _("Lisez les dernières actualités K-pop")
        canonical="/kpop"
        context = {
            "category_articles": page_obj,
            "category":category,
            "canonical":canonical,
            "language":language
        }
        return render(request, "webpage/category.html", context)
    return HttpResponseForbidden()

def kdrama(request, language="fr"):
    if request.method == "GET" and language in languages:
        translation.activate(language)
        # Restaurez la langue dans la requête (pour la prise en compte immédiate dans la vue actuelle)
        request.LANGUAGE_CODE = translation.get_language()

        all_articles = models.Article.objects.filter(Q(category="cinéma") | Q(category="Drama")).order_by("-pub_time")
        paginator = Paginator(all_articles, 25)
        page_number = request.GET.get("page")
        if page_number == "1":
            if language == "fr":
                return redirect("/kdrama", permanent=True)
            else:
                return redirect(f"/{language}/kdrama", permanent=True)
        page_obj = paginator.get_page(page_number)
        category = _("Lisez les dernières actualités K-drama")
        canonical="/kdrama"
        context = {
            "category_articles": page_obj,
            "category":category,
            "canonical":canonical,
            "language":language,
        }
        return render(request, "webpage/category.html", context)
    return HttpResponseForbidden()
    
def guide(request, language="fr"):
    if request.method == "GET" and language in languages:
        translation.activate(language)
        # Restaurez la langue dans la requête (pour la prise en compte immédiate dans la vue actuelle)
        request.LANGUAGE_CODE = translation.get_language()

        all_articles = models.Article.objects.filter(category__icontains="guide").order_by("-pub_time")
        paginator = Paginator(all_articles, 25)
        page_number = request.GET.get("page")
        if page_number == "1":
            if language == "fr":
                return redirect("/guide", permanent=True)
            else:
                return redirect(f"/{language}/guide", permanent=True)
        page_obj = paginator.get_page(page_number)
        category = _("Lisez les derniers guides rédigés sur la Corée du Sud")
        canonical="/guide"
        context = {
            "category_articles": page_obj,
            "category":category,
            "canonical":canonical,
            "language":language
        }
        return render(request, "webpage/category.html", context)
    return HttpResponseForbidden()

def faqs(request, language="fr"):
    if request.method == "GET" and language in languages:
        translation.activate(language)
        # Restaurez la langue dans la requête (pour la prise en compte immédiate dans la vue actuelle)
        request.LANGUAGE_CODE = translation.get_language()

        all_articles = models.Article.objects.filter(category__icontains="questions").order_by("-pub_time")
        paginator = Paginator(all_articles, 25)
        page_number = request.GET.get("page")
        if page_number == "1":
            if language == "fr":
                return redirect("/faqs", permanent=True)
            else:
                return redirect(f"/{language}/faqs", permanent=True)
        page_obj = paginator.get_page(page_number)
        category = _("Lisez les derniers questions-réponses rédigées sur la Corée du Sud, la Kpop, etc...")
        canonical="/faqs"
        context = {
            "category_articles": page_obj,
            "category":category,
            "canonical":canonical,
            "language":language
        }
        return render(request, "webpage/category.html", context)
    return HttpResponseForbidden()
    
def category(request, category, language="fr"):
    if request.method == "GET" and language in languages:
        translation.activate(language)
        # Restaurez la langue dans la requête (pour la prise en compte immédiate dans la vue actuelle)
        request.LANGUAGE_CODE = translation.get_language()
        category_articles = models.Article.objects.filter(category=category)
        paginator = Paginator(category_articles, 25)
        page_number = request.GET.get("page")
        if page_number == "1":
            if language == "fr":
                return redirect(f"/category/{category}", permanent=True)
            else:
                return redirect(f"/{language}/category/{category}", permanent=True)
        page_obj = paginator.get_page(page_number)
        canonical=f"/category/{category}"
        category = _(f"Lisez les dernières actualités") + " " + category
        context = {
            "category_articles": page_obj,
            "category":category,
            "canonical":canonical,
            "language":language
        }
        return render(request, "webpage/category.html", context)
    return HttpResponseForbidden()

def blog_detail(request, slug, language="fr"):
    if language in languages:
        translation.activate(language)
        # Restaurez la langue dans la requête (pour la prise en compte immédiate dans la vue actuelle)
        request.LANGUAGE_CODE = translation.get_language()

        pk = slug.split("-")[-1]
        if pk and pk.isdigit():
            try:
                article = get_object_or_404(models.Article, pk=pk)
            except:
                article = models.Article.objects.order_by("-pub_time").first()
                return redirect(f"/articles/{article.slug}", permanent=True)
        else:
            try:
                article = get_object_or_404(models.Article, slug=slug)
            except:
                article = models.Article.objects.filter(slug__icontains=slug.replace(pk, "")).first()
        
        if article and article.slug != slug:
            return redirect(f"/articles/{article.slug}", permanent=True)
        elif article is None:
            return redirect(f'/articles/{models.Article.objects.order_by("-pub_time").first().slug}', permanent=True)
        
        comments = models.Comment.objects.filter(article_pk=article.pk, in_reply_to__isnull=True, disabled=False)
        if comments:
            comments_count = comments.count()
        else:
            comments_count = 0
        
        related_articles = models.Article.objects.filter(category=article.category).exclude(pk=article.pk).order_by("-pk")[:5]
        selected_objects=None
        context = {
            "article": article,
            "selected_objects":selected_objects,
            "related_articles":related_articles,
            "language":language,
            "comments":comments,
            "comments_count":comments_count
        }
        if request.user.is_staff:
            response = render(request, "webpage/blog_detail.html", context)
            html_content = response.content.decode('utf-8')
            ratio = calculate_text_html_ratio(html_content)
            context["ratio"]=ratio
        if request.method == "GET":
            return render(request, "webpage/blog_detail.html", context)
        if request.method == "POST":
            email = request.POST.get("email","")
            username = request.POST.get("username","")
            comment = request.POST.get("comment","")
            in_reply_to = request.POST.get("in_reply_to","")
            if email and username and comment:
                if in_reply_to:
                    in_reply_to_comment = models.Comment.objects.get(pk=in_reply_to)
                    comment = models.Comment(
                        email=email,
                        username=username,
                        message=comment,
                        article_pk=article.pk,
                        in_reply_to=in_reply_to_comment
                    )
                else:
                    comment = models.Comment(
                        email=email,
                        username=username,
                        message=comment,
                        article_pk=article.pk
                    )
                comment.save()

                response = redirect(f"/articles/{article.slug}#comment_{article.pk}", permanent=True)
                response.set_cookie('username', username, max_age=31536000)
                response.set_cookie('email', email, max_age=31536000)
                return response
    return HttpResponseForbidden()


def blog_detail_pk(request, pk):
    if request.method == "GET":
        article = models.Article.objects.get(pk=pk)
        slug_article = slugify(f"{article.title[:120]}-{article.pk}")
        return redirect(f"/articles/{slug_article}", permanent=True)

def contact(request, language="fr"):
    if request.method == "POST":
        email = request.POST.get("email","")
        first_name = request.POST.get("first-name","")
        last_name = request.POST.get("last-name","")
        message = request.POST.get("message","")
        if email and first_name and last_name and message:
            contact = models.Contact(
                email=email,
                first_name=first_name,
                last_name=last_name,
                message=message,
            )
            contact.save()
            return render(request, "webpage/contact.html", {"success":True, "language":language})
    if request.method == "GET" and language in languages:
        translation.activate(language)
        # Restaurez la langue dans la requête (pour la prise en compte immédiate dans la vue actuelle)
        request.LANGUAGE_CODE = translation.get_language()
        return render(request, "webpage/contact.html", {"language":language})
    return HttpResponseForbidden()

def SearchResults(request, language="fr"):
    if request.method == 'GET' and language in languages:
        translation.activate(language)
        # Restaurez la langue dans la requête (pour la prise en compte immédiate dans la vue actuelle)
        request.LANGUAGE_CODE = translation.get_language()

        e = timezone.now().date()
        query = request.GET.get("q")
        search_words = query.split()
        article_list = models.Article.objects.filter(pub_time__date=e).order_by('-pub_time')

        # Liste des Q objects pour chaque mot
        q_objects = [Q(title__icontains=word) for word in search_words]
        object_list = models.Article.objects.filter(*q_objects).order_by('-pub_time')
        if not models.Article.objects.filter(*q_objects).exists():
            raise Http404()
        else:
            dealNumber = object_list.count()
            paginator = Paginator(object_list, 36)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'webpage/search_results.html', {'page_obj': page_obj, 'query': query, 'dealNumber':dealNumber, 'article_list':article_list, "language":language})
    return HttpResponseForbidden()


def mentionslegales(request, language="fr"):
    if request.method == "GET" and language in languages:
        translation.activate(language)
        # Restaurez la langue dans la requête (pour la prise en compte immédiate dans la vue actuelle)
        request.LANGUAGE_CODE = translation.get_language()
        return render(request, "webpage/mentionslegales.html", {"language":language})
    return HttpResponseForbidden()


@csrf_exempt
def cookies_accept(request):
    response = JsonResponse({'message': 'Cookies accepted'})
    response.set_cookie('cookie_accepted', True)
    response.set_cookie('cookie_banner', False)
    return response

def category_move(request):
    return redirect("/articles", permanent=True)

@login_required
def adminstats(request):
    if request.user.is_authenticated:
        date_list = [timezone.now().date() - timedelta(days=i) for i in range(7)]
        date = request.GET.get("date", timezone.now().date())
        unique_ips_today = models.Analytics.objects.filter(pub_time__date=date).values('ip').distinct().count()
        ip_summary = models.Analytics.objects.values('ip').annotate(count=Count('ip')).filter(count__gt=1, pub_time__date=date)
        ua_summary = models.Analytics.objects.values('ua').annotate(count=Count('ua')).filter(pub_time__date=date)
        referer_summary = models.Analytics.objects.values('referer').annotate(count=Count('referer')).filter(count__gt=1, pub_time__date=date).exclude(referer="None")
        utm_source_summary = models.Analytics.objects.values('utm_source').annotate(count=Count('utm_source')).filter(count__gt=1, pub_time__date=date).exclude(utm_source="").exclude(utm_source="None")
        url_summary = models.Analytics.objects.values('url').annotate(count=Count('url')).filter(count__gt=1, pub_time__date=date)
        context = {"unique_ips_today":unique_ips_today, 
                    "best_ua":ua_summary, 
                    "best_referers":referer_summary,
                    "best_utm":utm_source_summary,
                    "best_urls":url_summary,
                    "date_list":date_list,
                    "date":date
                    }
        return render(request, "webpage/adminstats.html", context)


def calculate_text_html_ratio(html_content):
    # Utilisez BeautifulSoup pour analyser le HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extraire le texte de la page
    text = soup.get_text()

    # Calculer la longueur du texte et du HTML
    text_length = len(text)
    html_length = len(html_content)

    # Calculer le ratio Text/HTML en pourcentage
    ratio_percentage = round((text_length / html_length) * 100, 1)

    return ratio_percentage

@csrf_exempt
def newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email","")
        if email and not models.Newsletter.objects.filter(email=email).exists():
            newsletter = models.Newsletter(
                email=email
            )
            newsletter.save()
            return JsonResponse({"status":"ok"}, status=200)
        else:
            return JsonResponse({"status":"Email manquant"}, status=400)
    return JsonResponse({"status":"Email manquant"}, status=400)
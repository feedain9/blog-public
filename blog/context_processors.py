from crawlerdetect import CrawlerDetect

allowed_hosts = ["domain.com"]
known_bots = ["Twitterbot", "facebookexternalhit", "facebookcatalog", "TelegramBot", 'Discordbot', 'Googlebot', 'GoogleOther', 'Google-InspectionTool', 'bingbot', 'bot', "InternetMeasurement", "Cloudflare-SSLDetector", "Mozilla/5.0 scpitspi-rs", "Python", "Chrome Privacy Preserving Prefetch Proxy", "MobileSafari/8617.1.17.10.9 CFNetwork/1490.0.4 Darwin/23.2.0", "undici"]
banned_refererdomain = ["127.0.0.1:8000"]
crawler_detect = CrawlerDetect()

primary_colors_dict = {
        'domain': 'domain.com',  # Couleur Body
        'name': '',  # Couleur Body
        'description': "",  # Couleur Body
        'paragraph1':"",
        'paragraph2':"",
        'paragraph3':"",
        'paragraph4':"",
        'instagram':'',
        'facebook':'',
        'twitter':'',
        'youtube':'',
        'pinterest':'',
        'tiktok':'',
        'color_body': '#FFFFFF',  # Couleur Body
        'color_primary': '#09002D',  # Couleur header/Footer
        'color_secondary': '#09002D',  # Couleur boutons/interactifs
        'color_tertiary': '#3F2D29',  # Couleur Texte
        'anchor':'#FFFFFF'
    }
def primary_colors(request):
    return primary_colors_dict

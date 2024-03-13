from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from . import models
import requests
import json
from google.oauth2 import service_account
import google.auth.transport.requests
from urllib.parse import quote
from .context_processors import primary_colors_dict
from django.template.defaultfilters import slugify
import os 
from PIL import Image
from io import BytesIO
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

@receiver(pre_delete, sender=models.Article)
def article_deleted(sender, instance, **kwargs):
    # Supprimez le fichier lorsque l'objet est supprimé
    if "thumbnail_default.jpg" not in str(instance.image_upload):
        instance.image_upload.delete(save=False)

import os
import random

from django import template
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone

register = template.Library()

@register.simple_tag
def random_images(request, count=8):
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    folder_path = 'photos/'  # Adjust this to the correct path within your media directory
    folder_abs_path = os.path.join(media_root, folder_path)
    
    image_files = [f for f in os.listdir(folder_abs_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    if 'chosen_images' not in request.session:
        request.session['chosen_images'] = []

    unused_images = [img for img in image_files if img not in request.session['chosen_images']]

    if not unused_images:
        request.session['chosen_images'] = []  # Reset if all images have been used
        unused_images = image_files

    chosen_images = random.sample(unused_images, min(count, len(unused_images)))
    request.session['chosen_images'].extend(chosen_images)
    
    request.session.save()
    
    image_info_list = []
    for chosen_image in chosen_images:
        chosen_image_url = f'{media_url}{folder_path}{chosen_image}'
        image_info_list.append({'url': chosen_image_url, 'path': chosen_image})
    
    return image_info_list

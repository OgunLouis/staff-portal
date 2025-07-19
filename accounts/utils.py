# accounts/utils.py
import requests
from django.conf import settings

def upload_to_imagekit(file):
    url = "https://upload.imagekit.io/api/v1/files/upload"
    auth = (settings.IMAGEKIT_PUBLIC_KEY, settings.IMAGEKIT_PRIVATE_KEY)
    data = {
        "fileName": file.name,
        "folder": "/profile_pics/",
    }
    files = {"file": file}

    response = requests.post(url, data=data, files=files, auth=auth)
    
    if response.status_code == 200:
        return response.json()['url']
    else:
        return None

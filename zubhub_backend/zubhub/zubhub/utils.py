# import requests
# from hashlib import sha256
# from lxml.html.clean import Cleaner
# import uuid
# from math import floor
# from pathlib import Path
# import re
# from django.utils.text import slugify
# from django.core.files.storage import Storage
# from django.core.files.base import ContentFile
# from django.utils.deconstruct import deconstructible
# from django.conf import settings
# from projects.tasks import delete_file_task


# def get_hash(string):
#     return sha256(string.encode("utf-8")).hexdigest()

# def get_upload_path(self, filename):
#     key = str(uuid.uuid4())
#     key = key[0: floor(len(key)/6)]
#     return '{0}/{1}-{2}'.format(self.MEDIA_PATH, slugify(filename), key)


# def get_sig(username, filename, upload_preset):
#     secret_hash = get_hash(settings.MEDIA_SECRET)
#     url = "http://media:8001/sigen/"
#     return requests.post(url, data={"username": username,
#                                     "filename": filename, "upload_preset": upload_preset,
#                                     "secret_hash": secret_hash})


# def get_cloudinary_resource_info(resource_url):
#     secret_hash = get_hash(settings.MEDIA_SECRET)
#     url = 'http://media:8001/get-cloudinary-resource-info/'
#     return requests.post(url, data={'url': resource_url, "secret_hash": secret_hash})


# def upload_file_to_media_server(file, key):
#     secret_hash = get_hash(settings.MEDIA_SECRET)
#     url = 'http://media:8001/upload-file/'
#     _, name = key.split("/")
#     files = {}
#     files[name] = file
#     return requests.post(url, data={'key': key, "secret_hash": secret_hash}, files=files)


# def delete_file_from_media_server(file_url):
#     secret_hash = get_hash(settings.MEDIA_SECRET)
#     url = 'http://media:8001/delete-file/'
#     return requests.post(url, data={'url': file_url, "secret_hash": secret_hash})



# """ Clean summermote html while still allowing for basic html structure """
# def clean_summernote_html(string):
#     cleaner = Cleaner()
#     return cleaner.clean_html(string)


# def replace_summernote_images_with_media_storage_equiv(text):
#     """ 
#     Extract all summernote image paths in the html text,
#     upload them to media storage server,
#     and replace them with the response url from the media storage server
#     """
#     regex = r'<img[^<>]+src=["\']/api/media/([^"\'<>]+\.(?:gif|png|jpe?g))["\']'
#     temp_image_paths = re.findall(regex, text, re.I) # e.g. ["django-summernote/2023-09-03/image.jpg", "django-summernote/2023-09-03/image2.jpg"]
#     for temp_image_path in temp_image_paths:
#         path = Path(settings.MEDIA_ROOT, temp_image_path)
#         with path.open(mode="rb") as file:
#             key = get_upload_path(
#                 type('', (object,), {'MEDIA_PATH': 'zubhub'}),
#                 slugify(path.name)
#             )
#             image_url = upload_file_to_media_server(file=file, key=key).json()["url"]
#             full_temp_image_url = settings.MEDIA_URL + str(temp_image_path)
#             text = image_url.join(text.split(full_temp_image_url))
#         path.unlink()
#     return text





# #========================= Docs helper functions =======================
# def get_media_schema():
#     """ Get API Schema Of Media Server """

#     secret_hash = get_hash(settings.MEDIA_SECRET)
#     url = 'http://media:8001/media-schema/'
#     return requests.post(url, data={"secret_hash": secret_hash})

# def get_image_paths(html):
#     """ 
#     Get all image names in html image tag
    
#     Returns ["string"]
#     e.g. ["image.jpg", "image2.png", "image3.jpg"]
#     """
#     import re
    
#     try:
#         paths =  re.findall(r'<img[^<>]+src=["\']./([^"\'<>]+\.(?:gif|png|jpe?g))["\']', html, re.I)
#         return paths
#     except Exception as e:
#         return []

# def images_to_base64(paths, html):
#     """ Replace all image names in html image tag with the base64 string of corresponding image """

#     from os import path
#     from base64 import b64encode

#     try:
#         for image in paths: # path contains image file names e.g. one.jpg, two.png 
#             image_path = path.join(settings.BASE_DIR, 'docs', 'docs', image) # get image full path
#             with open(image_path, "rb") as file:
#                 base64_data = b64encode(file.read())
#                 html = html.replace("./" + image, "data:image/png;base64," + base64_data.decode()) #replace image path with base64 string
#         return html
#     except Exception as e:
#         return html
# #==================================================================================

    
# @deconstructible
# class MediaStorage(Storage):
#     def __eq__(self, other):
#         return False

#     def _open(self, name, _):
#         res = requests.get(name)
#         return ContentFile(res.content)

#     def _save(self, name, content):
#         res = upload_file_to_media_server(content, name)
#         res = res.json()["url"]

#         if isinstance(res, str):
#             return res
#         else:
#             raise Exception()

#     def delete(self, name):
#         delete_file_task.delay(name)

#     def get_available_name(self, name, max_length):
#         return name

#     def url(self, name):
#         return name
import requests
from hashlib import sha256
from lxml.html.clean import Cleaner
import uuid
from math import floor
from pathlib import Path
import re
from django.utils.text import slugify
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
from django.conf import settings
from projects.tasks import delete_file_task
from base64 import b64encode
from os import path


def get_hash(string):
    """Generate a SHA256 hash for a given string."""
    return sha256(string.encode("utf-8")).hexdigest()


def get_upload_path(self, filename):
    """Generate a unique upload path for the given filename."""
    key = str(uuid.uuid4())[:floor(len(key) / 6)]
    return f'{self.MEDIA_PATH}/{slugify(filename)}-{key}'


def get_sig(username, filename, upload_preset):
    """Request a signature for uploading to media server."""
    secret_hash = get_hash(settings.MEDIA_SECRET)
    url = "http://media:8001/sigen/"
    response = requests.post(url, data={"username": username, "filename": filename, "upload_preset": upload_preset, "secret_hash": secret_hash})
    response.raise_for_status()  # Raise an error for bad responses
    return response


def get_cloudinary_resource_info(resource_url):
    """Retrieve resource info from Cloudinary."""
    secret_hash = get_hash(settings.MEDIA_SECRET)
    url = 'http://media:8001/get-cloudinary-resource-info/'
    response = requests.post(url, data={'url': resource_url, "secret_hash": secret_hash})
    response.raise_for_status()  # Raise an error for bad responses
    return response


def upload_file_to_media_server(file, key):
    """Upload a file to the media server and return the response."""
    secret_hash = get_hash(settings.MEDIA_SECRET)
    url = 'http://media:8001/upload-file/'
    _, name = key.split("/")
    files = {name: file}
    response = requests.post(url, data={'key': key, "secret_hash": secret_hash}, files=files)
    response.raise_for_status()  # Raise an error for bad responses
    return response


def delete_file_from_media_server(file_url):
    """Delete a file from the media server."""
    secret_hash = get_hash(settings.MEDIA_SECRET)
    url = 'http://media:8001/delete-file/'
    response = requests.post(url, data={'url': file_url, "secret_hash": secret_hash})
    response.raise_for_status()  # Raise an error for bad responses
    return response


def clean_summernote_html(string):
    """Clean HTML content while allowing basic HTML structure."""
    cleaner = Cleaner()
    return cleaner.clean_html(string)


def replace_summernote_images_with_media_storage_equiv(text):
    """
    Replace summernote image paths in the HTML text with URLs from media storage server.
    Upload images to media storage and return updated HTML.
    """
    regex = r'<img[^<>]+src=["\']/api/media/([^"\'<>]+\.(?:gif|png|jpe?g))["\']'
    temp_image_paths = re.findall(regex, text, re.I)
    
    for temp_image_path in temp_image_paths:
        path_to_image = Path(settings.MEDIA_ROOT, temp_image_path)
        if path_to_image.exists():
            with path_to_image.open(mode="rb") as file:
                key = get_upload_path(type('', (object,), {'MEDIA_PATH': 'zubhub'}), slugify(path_to_image.name))
                image_url = upload_file_to_media_server(file=file, key=key).json()["url"]
                full_temp_image_url = settings.MEDIA_URL + str(temp_image_path)
                text = image_url.join(text.split(full_temp_image_url))
            path_to_image.unlink()
    return text


#========================= Docs helper functions =======================
def get_media_schema():
    """Get API Schema of Media Server."""
    secret_hash = get_hash(settings.MEDIA_SECRET)
    url = 'http://media:8001/media-schema/'
    response = requests.post(url, data={"secret_hash": secret_hash})
    response.raise_for_status()  # Raise an error for bad responses
    return response


def get_image_paths(html):
    """Extract all image paths from HTML image tags."""
    try:
        paths = re.findall(r'<img[^<>]+src=["\']./([^"\'<>]+\.(?:gif|png|jpe?g))["\']', html, re.I)
        return paths
    except Exception:
        return []


def images_to_base64(paths, html):
    """Replace image paths in HTML with their base64 string representations."""
    try:
        for image in paths:
            image_path = path.join(settings.BASE_DIR, 'docs', 'docs', image)
            with open(image_path, "rb") as file:
                base64_data = b64encode(file.read())
                html = html.replace("./" + image, f"data:image/png;base64,{base64_data.decode()}")
        return html
    except Exception:
        return html


#==================================================================================

@deconstructible
class MediaStorage(Storage):
    """Custom storage backend for media files."""
    
    def __eq__(self, other):
        return False

    def _open(self, name, _):
        """Open and return the content of the file."""
        res = requests.get(name)
        res.raise_for_status()  # Raise an error for bad responses
        return ContentFile(res.content)

    def _save(self, name, content):
        """Save a file to the media server and return its URL."""
        response = upload_file_to_media_server(content, name)
        res_url = response.json().get("url")

        if isinstance(res_url, str):
            return res_url
        else:
            raise Exception("Failed to save file: Invalid response")

    def delete(self, name):
        """Delete the file using a background task."""
        delete_file_task.delay(name)

    def get_available_name(self, name, max_length):
        """Get the available name for the file."""
        return name

    def url(self, name):
        """Return the URL for the file."""
        return name


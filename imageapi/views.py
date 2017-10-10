import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from imageapi.renderers import ImageRenderer


class ImageInfo(APIView):
    def post(self, request):
        ''' POST method for creating a new image'''
        imageformats = ["jpeg", "JPEG", "jpg", "JPG", "png", "PNG",\
                       "gif", "GIF", "bmp", "BMP", "tiff", "TIFF"]    # All valid image formats
        if 'file' in request.FILES:
            file = request.FILES['file']
            base, ext = os.path.splitext(file.name)
            ext = ext[1:]                    # Getting extension of uploaded file
            if not ext in imageformats:      # Checking whether the extension is valid or not.This checking can be omitted.                          
                content = {
                    "message": "UnSupported/Invalid image format!!"
                }
                return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
            username = request.user.username
            location = os.path.join(settings.MEDIA_ROOT, username)
            file_storage = FileSystemStorage(location=location)
            filename = file_storage.save(file.name, file)         # Saving file to media/username folder
            content = {
                "message": filename+" uploaded successfully!!"
            }
            return JsonResponse(content, status=status.HTTP_201_CREATED)

    def get(self, request):
        ''' GET method for getting all images linked to the provided access key'''
        username = request.user.username
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, username)):        # Checking whether folder media/username exits or not
            images = os.listdir(os.path.join(settings.MEDIA_ROOT, username))
            content = []
            for image in images:
                content.append({
                    "filename": image
                })
            return JsonResponse(content, status=status.HTTP_200_OK, safe=False)
        else:
            content = {
                "message": "Requested folder media/"+username+" does'nt exists!!"
            }
            return JsonResponse(content, status=status.HTTP_404_NOT_FOUND)


class ImageDetail(APIView):
    renderer_classes = (ImageRenderer, JSONRenderer)

    def get(self, request, img):
        ''' GET method for displaying the requested image'''
        username = request.user.username
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, username)):
            images = os.listdir(os.path.join(settings.MEDIA_ROOT, username))
            if img in images:
                path = os.path.join(settings.MEDIA_ROOT, username, img)
                image = open(path, "rb").read()
                base, ext = os.path.splitext(path)
                ext = ext[1:]                    # Getting extension of uploaded file
                return Response(image, content_type="image/"+ext)
            else:
                content = {
                    "message": "File not found in request"
                }
                return JsonResponse(content, status=status.HTTP_404_NOT_FOUND)
        else:
            content = {
                "message": "Requested folder media/"+username+" does'nt exists!!"
            }
            return JsonResponse(content, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, img):
        ''' PATCH method for updating the requested image with the uploaded image'''
        imageformats = ["jpeg", "JPEG", "jpg", "JPG", "png", "PNG", \
                       "gif", "GIF", "bmp", "BMP", "tiff", "TIFF"]
        username = request.user.username
        images = os.listdir(os.path.join(settings.MEDIA_ROOT, username))
        if img in images:
            if 'file' in request.FILES:
                file = request.FILES['file']
                base, ext = os.path.splitext(file.name)
                ext = ext[1:]                     # Getting extension of uploaded file
                if not ext in imageformats:       # Checking whether the extension is valid or not.This checking can be omitted.
                    content = {
                        "message": "UnSupported/Invalid image format!!"
                    }
                    return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
                path = os.path.join(settings.MEDIA_ROOT, username, img)
                os.remove(path)                      # Removing the requested file
                location = os.path.join(settings.MEDIA_ROOT, username)
                file_storage = FileSystemStorage(location=location)
                filename = file_storage.save(img, file)        # Saving the uploaded file with the name of requested file
                content = {
                    "message": filename + " updated successfully!!"
                }
                return JsonResponse(content, status=status.HTTP_200_OK)
        else:               # Condition for requested file not found.
            content = {
                "message": "File not found in request"
            }
            return JsonResponse(content, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, img):
        ''' DELETE method for deleting the requested image '''
        username = request.user.username
        images = os.listdir(os.path.join(settings.MEDIA_ROOT, username))
        if img in images:
            path = os.path.join(settings.MEDIA_ROOT, username, img)
            os.remove(path)                             # Removing the requested file.
            content = {
                "message": img+" was deleted successfully."
            }
            return JsonResponse(content, status=status.HTTP_200_OK)
        else:                     # Condition for requested file not found.
            content = {
                "message": "File not found in request"
                }
            return JsonResponse(content, status=status.HTTP_404_NOT_FOUND)

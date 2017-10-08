from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from imageapi.renderers import ImageRenderer
from rest_framework.renderers import JSONRenderer
import os
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

class ImageInfo(APIView):
    def post(self, request):
        if 'file' in request.FILES:
            file = request.FILES['file']
            username = request.user.username
            location = os.path.join(settings.MEDIA_ROOT, username)
            fs = FileSystemStorage(location=location)
            filename = fs.save(file.name, file)
            content = {
                "message": filename+" uploaded successfully!!"
            }
            return JsonResponse(content, status=status.HTTP_201_CREATED)
        else:
            content = {
                "message": "File not found in request"
            }
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        username = request.user.username
        images = os.listdir(os.path.join(settings.MEDIA_ROOT, username))
        content = []
        for image in images:
            content.append({
                "filename": image
            })
        return JsonResponse(content,status=status.HTTP_200_OK,safe=False)


class ImageDetail(APIView):
    renderer_classes = (ImageRenderer,JSONRenderer)

    def get(self, request, img):
        username = request.user.username
        images = os.listdir(os.path.join(settings.MEDIA_ROOT, username))
        if img in images:
            path = os.path.join(settings.MEDIA_ROOT, username, img)
            image = open(path, "rb").read()
            base,ext=os.path.splitext(path)
            ext=ext[1:]
            return Response(image, content_type="image/"+ext)
        else:
            content={
                "message":"File not found in request"
            }
            return JsonResponse(content,status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, img):
        username = request.user.username
        images = os.listdir(os.path.join(settings.MEDIA_ROOT, username))
        if img in images:
            path = os.path.join(settings.MEDIA_ROOT, username, img)
            os.remove(path)
            if 'file' in request.FILES:
                file = request.FILES['file']
                location = os.path.join(settings.MEDIA_ROOT, username)
                fs = FileSystemStorage(location=location)
                filename = fs.save(img, file)
                content = {
                    "message": filename +" updated successfully!!"
                }
                return JsonResponse(content,status=status.HTTP_200_OK)
            else:
                content = {
                    "message": "File not found in request"
                }
                return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            content={
                "message":"File not found in request"
            }
            return JsonResponse(content,status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, img):
        username = request.user.username
        images = os.listdir(os.path.join(settings.MEDIA_ROOT, username))
        if img in images:
            path = os.path.join(settings.MEDIA_ROOT, username, img)
            os.remove(path)
            content={
                "message": img+" was deleted successfully."
            }
            return JsonResponse(content,status=status.HTTP_200_OK)
        else:
            content = {
                    "message": "File not found in request"
                }
            return JsonResponse(content,status=status.HTTP_404_NOT_FOUND)
from django.http import HttpResponse

from test_app.models import Image


def test_img(request):
    return HttpResponse([i.image.url for i in Image.objects.all()])

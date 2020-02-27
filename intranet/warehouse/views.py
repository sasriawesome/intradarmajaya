from django.shortcuts import HttpResponse
from .tasks import send_html_email


def test_dramatiq(request):
    send_html_email("Cuma Test", "sasri.gg@gmail.com", ["sasri.darmajaya@gmail.com"], "Yada Yada OK")
    return HttpResponse('Email sent')

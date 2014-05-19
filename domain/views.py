from django.http import HttpResponse


def domain_home(request):

    return HttpResponse('Hello Home')
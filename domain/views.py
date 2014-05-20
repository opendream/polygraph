from django.shortcuts import render


def domain_home(request):

    return render(request, 'domain/domain_home.html', {})

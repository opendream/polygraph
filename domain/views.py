from django.shortcuts import render


def domain_home(request):

    return render(request, 'domain/home.html', {})


def domain_statement_list(request):

    return render(request, 'domain/statement_list.html', {})

def domain_statement_detail(request, statement_permalink):

    return render(request, 'domain/statement_detail.html', {statement_permalink: statement_permalink})
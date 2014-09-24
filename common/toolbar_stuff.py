
def custom_show_toolbar(request):
    print request.path
    if '/item/' in request.path:
        return False
    return True
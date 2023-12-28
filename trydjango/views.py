"""
To render html web pages
"""

from django.http import HttpResponse



def home_view(request):
    """
    Take in a request
    Return HTML as response
    """
    name = request.GET['name']
    print(name)
    HTML_STRING = f"""
    <h1>Hello {name}</h1>
    """
    return HttpResponse(HTML_STRING)
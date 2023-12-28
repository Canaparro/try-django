"""
To render html web pages
"""

from django.http import HttpResponse



def home_view(request):
    """
    Take in a request
    Return HTML as response
    """
    
    HTML_Title = f"""
    <h1>{title}</h1>
    """

    HTML_content = f"""
    <h1>Hello {content}</h1>
    """
    return HttpResponse(HTML_STRING)
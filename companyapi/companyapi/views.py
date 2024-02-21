from django.http import HttpResponse,JsonResponse


def home_page(request):
    print('Home page Requested')
    friends=['ankit', 'ravi','uttam']
    return JsonResponse(friends,safe=False)

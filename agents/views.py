# from django.http import JsonResponse
# from .models import City

# def get_cities(request):
#     country_id = request.GET.get("country")  # Get country_id from request
#     print('country_id:', country_id)
#     if country_id:
#         cities = City.objects.filter(country_id=country_id).values("id", "name")
#         print('cities:', list(cities))
#         response = JsonResponse(list(cities), safe=False)
#         print('response:', response)
#         return response
#     return JsonResponse([], safe=False)

from django.http import JsonResponse
from .models import City

def get_cities(request):
    country_id = request.GET.get("country")
    if not country_id:
        return JsonResponse({"error": "Missing country parameter"}, status=400)

    cities = list(City.objects.filter(country_id=country_id).values("id", "name"))
    return JsonResponse(cities, safe=False)


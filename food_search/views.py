from django.shortcuts import render
from django.conf import settings
from .models import *
import requests
import json


def find_food(request):
    # ingredients = ownedIngredients.objects.all().values("name")
    # ignoredIngredients = ignoredIngredients.objects.all().values("name")

    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    paramsAPI = {"ingredients": ownedIngredients.objects.all().values_list('name', flat=True),
                 "ignorePantry": ignoredIngredients.objects.all().values_list('name', flat=True),
                 "number": "2",
                 "apiKey": settings.SPOONACULAR_API_KEY}
    errors = []

    # response = requests.get('https://api.spoonacular.com/recipes/findByIngredients?ingredients=apples,+flour,+sugar&number=2&apiKey=%s' % settings.SPOONACULAR_API_KEY)


    try:
        response = requests.get(url=url, params=paramsAPI).json()
    except requests.exceptions.HTTPError as errh:
        errors.append(errh)
    except requests.exceptions.ConnectionError as errc:
        errors.append(errc)
    except requests.exceptions.Timeout as errt:
        errors.append(errt)
    except requests.exceptions.RequestException as err:
        errors.append(err)
    finally:

        for recip in response:
            print("title: %s\n image: %s\n usedIngredients: %s" % (recip["title"], recip["image"], recip["usedIngredients"][0]["name"]))

            # recip = recipes(name = response[])

        return render(request, 'food_search.html', {
            'errorResponse': errors,
            'response': response,
        })
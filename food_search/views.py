from django.shortcuts import render
from django.conf import settings
from .models import *
import requests
import json


def find_food(request):

    paramsAPI = {"ingredients": ["apples","+flour","+sugar"], #dorobić sczytywanie z podawanej wcześniej listy
                 "ignorePantry": ["plumbs"], #dorobić sczytywanie z podawanej wcześniej listy
                 "number": "2",
                 "apiKey": settings.SPOONACULAR_API_KEY}
    errors = []

    # response = requests.get('https://api.spoonacular.com/recipes/findByIngredients?ingredients=apples,+flour,+sugar&number=2&apiKey=%s' % settings.SPOONACULAR_API_KEY)

    try:
        response = requests.get(url='https://api.spoonacular.com/recipes/findByIngredients', params=paramsAPI).json()
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
            nutritionURL = 'https://api.spoonacular.com/recipes/{id}/nutritionWidget.json'.format(id=recip["id"])
            nutritionData = requests.get(url = nutritionURL, params={"apiKey": settings.SPOONACULAR_API_KEY}).json()
            newRecip = recipes(name=recip["title"], image=recip["image"], carbs=nutritionData["carbs"], proteins=nutritionData["protein"], calories=nutritionData["calories"])
            newRecip.save()

            #Adding used ingredients
            for ingredient in recip["usedIngredients"]:
                newIngredient = missingIngredients(name = ingredient['name'], recip = newRecip)
                newIngredient.save()

            #Adding missing ingredients
            for ingredient in recip["missedIngredients"]:
                newIngredient = missingIngredients(name = ingredient['name'], recip = newRecip)
                newIngredient.save()


        return render(request, 'food_search.html', {
            'errorResponse': errors,
            'response': recipes.objects.all(),
        })

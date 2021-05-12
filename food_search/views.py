from django.shortcuts import render, redirect
from django.conf import settings

from .models import *
import requests



def home(request):
    errors, request.session['owned_ingredients'], request.session['ignoredIngredients'] = [], [], []

    if request.method == 'POST':
        request.session['owned_ingredients'] = request.POST.get('owned_ingredients')
        request.session['ignored_ingredients'] = request.POST.get('ignored_ingredients')
        return redirect('myapp:find_food')

    else:
        return render(request, 'food_search.html', {
            'error_response': [],
            'recips_data': [],
            'owned_ingredients': [],
            'missing_ingredients': []
        })


def find_food(request):
    paramsAPI = {"ingredients": request.session['owned_ingredients'],
                 "ignorePantry": request.session['ignored_ingredients'],
                 "number": "1",
                 "apiKey": settings.SPOONACULAR_API_KEY}
    errors = []
    recips_ids = []

   #Lista wszystkich recip_api_id
   # recipes.objects.values_list('recip_api_id', flat=True).distinct()

   #get recip_api_id from ownedIngredients
   #ownedIngredients.recip.get_queryset().values_list('recip_api_id', flat=True)

    try: #try to connect with api
        response = requests.get(url='https://api.spoonacular.com/recipes/findByIngredients', params=paramsAPI).json()
    except Exception as e:
        errors.append(e)
    else: #if there is no error
        for recip in response:
            recips_ids.append(recip["id"])

            # if we don't have recip in DB, add one:
            if not recipes.objects.filter(recip_api_id=recip["id"]).exists():
                nutritionURL = 'https://api.spoonacular.com/recipes/{id}/nutritionWidget.json'.format(id=recip["id"])
                nutritionData = requests.get(url=nutritionURL, params={"apiKey": settings.SPOONACULAR_API_KEY}).json()
                newRecip = recipes(recip_api_id=recip["id"], name=recip["title"], image=recip["image"], carbs=nutritionData["carbs"],
                                   proteins=nutritionData["protein"], calories=nutritionData["calories"])

                newRecip.save()


                # Adding used ingredients
                for ingredient in recip['usedIngredients']:
                    newIngredient = ownedIngredients(name=ingredient['name'], recip=newRecip)
                    newIngredient.save()

                # Adding missing ingredients
                for ingredient in recip['missedIngredients']:
                    newIngredient = missingIngredients(name=ingredient['name'], recip=newRecip)
                    newIngredient.save()

    finally: #always run this:
        return render(request, 'food_search.html', {
            'error_response': errors,
            'recips_data': recipes.objects.filter(recip_api_id__in=recips_ids).order_by('proteins'),
            'owned_ingredients': ownedIngredients.objects.all(),
            'missing_ingredients': missingIngredients.objects.all()
        })

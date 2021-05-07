from django.db import models

class ownedIngredients(models.Model):
    name = models.CharField(max_length=64)
    carbohydrates = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()

class ignoredIngredients(models.Model):
    name = models.CharField(max_length=64)
    carbohydrates = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()

class missingIngredients(models.Model):
    name = models.CharField(max_length=64)
    carbohydrates = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()

class recipes(models.Model):
    name = models.CharField(max_length=64)
    image = models.CharField(max_length=255)
    ownedIngredients = models.CharField(max_length=255)
    missingIngredients = models.CharField(max_length=255)
    carbohydrates = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()
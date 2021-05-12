from django.db import models

class recipes(models.Model):
    recip_api_id = models.IntegerField()
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    carbs = models.CharField(max_length=10)
    proteins = models.CharField(max_length=10)
    calories = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ownedIngredients(models.Model):
    name = models.CharField(max_length=64)
    recip =  models.ForeignKey(recipes, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['recip']


class missingIngredients(models.Model):
    name = models.CharField(max_length=64)
    recip =  models.ForeignKey(recipes, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['recip']


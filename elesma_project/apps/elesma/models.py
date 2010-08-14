from django.db import models

class Category(models.Model):
    
    name = models.CharField(max_length=36)
    
    def __unicode__(self):
        return self.name


class Container(models.Model):
    
    name = models.CharField(max_length=36)
    
    def __unicode__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(max_length=36)

    def __unicode__(self):
        return self.name


class Recipe(models.Model):

    name = models.CharField(max_length=36)
    slug = models.SlugField(unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    directions = models.TextField(blank=True)
    category = models.ForeignKey(Category)
    container = models.ForeignKey(Container)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeItem')
    
    def __unicode__(self):
        return self.name


class RecipeItem(models.Model):

    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.CharField(max_length=24)
    
    def __unicode__(self):
        return "%s of %s" % (self.amount, self.ingredient)

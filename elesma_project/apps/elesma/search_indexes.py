import datetime
from haystack.indexes import *
from haystack import site
from elesma.models import Recipe, Ingredient
import settings

SEARCH_INDEX_CLASS = (settings.DEBUG and RealTimeSearchIndex) or SearchIndex

class RecipeIndex(SEARCH_INDEX_CLASS):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name')
    slug = CharField(model_attr='slug')
    
    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Recipe.objects.all()

class IngredientIndex(SEARCH_INDEX_CLASS):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Ingredient.objects.all()

site.register(Recipe, RecipeIndex)
site.register(Ingredient, IngredientIndex)

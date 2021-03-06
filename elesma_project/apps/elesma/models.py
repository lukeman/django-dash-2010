from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from djangoratings.fields import RatingField
from taggit.managers import TaggableManager



class UserProfile(models.Model):
    "Store voting information about user."

    user = models.ForeignKey(User, unique=True)
    votes = models.IntegerField()

    def __unicode__(self):
        try:
            return "UserProfile(%s)" % (self.user.username,)
        except:
            return "UserProfile"

    def get_absolute_url(self):
        return reverse("user_profile", kwargs={
                "username": self.user.username,
                })

def user_post_save(sender, instance, **kwargs):
    try:
        profile, new = UserProfile.objects.get_or_create(user=instance, votes=0)
    except:
        pass

def user_post_delete(sender, instance, **kwargs):
    try:
        UserProfile.objects.get(user=instance).delete()
    except:
        pass

models.signals.post_save.connect(user_post_save, sender=User)
models.signals.post_delete.connect(user_post_delete, sender=User)


class Category(models.Model):
    
    name = models.CharField(max_length=72)
    
    def __unicode__(self):
        return self.name


class Container(models.Model):
    
    name = models.CharField(max_length=72)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="elesma/container", blank=True)
    url = models.URLField(blank=True, verify_exists=False)
    
    def __unicode__(self):
        return self.name


class Ingredient(models.Model):
    
    # TODO - Finish this list
    TYPE_OF_INGREDIENT_CHOICES = (
        ('SP', 'Spirit'),
        ('LQ', 'Liqueur'),
        ('GR', 'Garnish'),
    ) 

    name = models.CharField(max_length=72)
    ingredient_type = models.CharField(blank=True, max_length=2,
                            choices=TYPE_OF_INGREDIENT_CHOICES)

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return "%s?ingredient=%s" % (reverse("ingredient_detail"), self.name)

class Recipe(models.Model):

    name = models.CharField(max_length=72)
    slug = models.SlugField(unique=True, null=False, blank=False)
    photo = models.ImageField(upload_to="elesma/recipe", blank=True)
    description = models.TextField(blank=True)
    directions = models.TextField(blank=True)
    category = models.ForeignKey(Category)
    container = models.ForeignKey(Container)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeItem')
    tags = TaggableManager()
    rating = RatingField(range=5, can_change_vote=True, allow_anonymous=False)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
            return reverse("recipe_detail", kwargs={
                "slug": self.slug,
            })


class RecipeItem(models.Model):

    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.CharField(max_length=24)
    
    def __unicode__(self):
        return "%s %s" % (self.amount, self.ingredient)

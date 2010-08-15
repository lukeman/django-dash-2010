from django.db import models
from taggit.managers import TaggableManager
from djangoratings.fields import RatingField
from django.contrib.auth.models import User

class UserProfile(models.Model):
    "Store voting information about user."

    user = models.ForeignKey(User, unique=True)
    votes = models.IntegerField()

    def __unicode__(self):
        return "UserProfile(%s)" % (self.user.username,)


def user_post_save(sender, instance, **kwargs):
    profile, new = UserProfile.objects.get_or_create(user=instance, votes=0)

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
    
    def __unicode__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(max_length=72)

    def __unicode__(self):
        return self.name


class Recipe(models.Model):

    name = models.CharField(max_length=72)
    slug = models.SlugField(unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    directions = models.TextField(blank=True)
    category = models.ForeignKey(Category)
    container = models.ForeignKey(Container)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeItem')
    tags = TaggableManager()
    rating = RatingField(range=5, can_change_vote=True, allow_anonymous=False)
    
    def __unicode__(self):
        return self.name


class RecipeItem(models.Model):

    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.CharField(max_length=24)
    
    def __unicode__(self):
        return "%s of %s" % (self.amount, self.ingredient)
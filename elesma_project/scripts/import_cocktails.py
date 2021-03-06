import elesma.models
import django.utils.simplejson as simplejson
from django.template.defaultfilters import slugify
import os.path

def import_cocktails(filename=None):
    "Load all cocktails from JSON file into database."
    if not filename:
        from settings import PROJECT_ROOT
        filename = os.path.join(PROJECT_ROOT, "scripts", "drinks.json")

    with open(filename, 'r') as fin:
        raw = fin.read()
        cocktails = simplejson.loads(raw)
        for cocktail in cocktails:
            import_cocktail(cocktail)

def import_cocktail(cocktail):
    """
    Load a cocktail from dictionary into database.

    {'group': 'AFTER-DINNER',
     'name': 'RUSTY NAIL', 
     'img': 'http://www.iba-world.com/english/cocktails/img/cocktails/rusty-nail.jpg', 
     'ingredients': [{'units': 'cl', 'name': 'Scotch whisky', 'qty': '4.5'},
                     {'units': 'cl', 'name': 'Drambuie', 'qty': '2.5'}],
     'glass': 'After dinner ( old fashioned glass)',
     'instructions': 'Pour all ingredients directly into old fashioned glass filled with ice. Stir gently. Garnish with lemon twist.'
     }
    """
    if not cocktail['name'] or len(cocktail['glass']) > 70:
        print "BAD DATA: %s" % (cocktail,)
        return
    else:
        for ingredient in cocktail['ingredients']:
            if len(ingredient['name']) > 70:
                print "BAD DATA: %s" % (cocktail,)
                return
    
    # create/update category
    try: 
        category = elesma.models.Category.objects.get(name=cocktail['group'])
    except:
        category = elesma.models.Category.objects.create(name=cocktail['group'])

    glass = cocktail['glass'].split('(')[-1][:-1].upper().split('OR')[-1].strip().replace('  ',' ').replace('COCKTIAL','COCKTAIL')
    try: 
        container = elesma.models.Container.objects.get(name=glass)
    except:
        container = elesma.models.Container.objects.create(name=glass)

    print cocktail
    try:
        ctl = elesma.models.Recipe.objects.create(container=container,
                                                  slug=slugify(cocktail['name']),
                                                  category=category,
                                                  name=cocktail['name'],
                                                  directions=cocktail['instructions'],
                                                  )
    except:
        ctl = elesma.models.Recipe.objects.get(slug=cocktail['name'].lower().replace(' ','-'))

    # missing ingredients & recipe items
    # add ingredients to the cocktail
    ingredients = []
    for ingredient in cocktail['ingredients']:
        # 'ingredients': [{'units': 'cl', 'name': 'Scotch whisky', 'qty': '4.5'},
        #             {'units': 'cl', 'name': 'Drambuie', 'qty': '2.5'}],
        ingredient_name = ingredient['name'].replace('of ','').strip().replace('&eacute;','e').replace('&egrave;','e').lower().replace('bitters', 'bitter')
        if ingredient_name.find('lemon') != -1 and ingredient_name.find('lime') != -1:
            ingredient_name = "lemon juice or lime juice"

        if ingredient_name:
            try: 
                ingredients.append(elesma.models.Ingredient.objects.get(name=ingredient_name))
            except:
                ingredients.append(elesma.models.Ingredient.objects.create(name=ingredient_name))

            try: 
                elesma.models.RecipeItem.objects.get(recipe=ctl, ingredient=ingredients[-1])
            except:
                qty = "%s %s" % (ingredient['qty'], ingredient['units'])
                elesma.models.RecipeItem.objects.create(recipe=ctl, ingredient=ingredients[-1], amount=qty)




from models import Recipe, Ingredient, Category, Container, RecipeItem, UserProfile
from django.contrib import admin

class RecipeItemInline(admin.TabularInline):
    
    model = RecipeItem
    extra = 4


class RecipeAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {"slug": ("name",)}
    inlines = (RecipeItemInline,)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(Container)
admin.site.register(UserProfile)

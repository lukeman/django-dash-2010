
## Install Recipes Fixture

    ./manage.py loaddata fixtures/recipes.json

## Setup Search

    ./manage.py update_index
    ./manage.py runserver
    http://localhost:8000/search/?q=russian&models=elesma.recipe


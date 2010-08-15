"""
File to contain utility functions which will power the various views in sundry ways.
"""

def search_recipes(query, offset=0, count=10):
    """
    Search for only recipes (e.g. not ingredients or other indexes).

    Intended for usage on the primary results page.
    """
    return []

def get_user_leaderboard(offset=0, count=10):
    """
    Return users ordered by number of votes.

    Intended for usage on the leaderboard page(s).
    """
    return []

def get_user_votes(user, offset=0, count=10):
    """
    Retrieve votes for user, sorted by recency.

    Intended for use either in a profile page or as a common module.
    """
    return []

def get_popular_recipes(offset=0, count=10):
    """
    Return recipes ordered by voting scores.

    Intended for use on eitiher a stand-alone page or as module on drink page.
    """
    return []

def get_related_recipes(recipe, offset=0, count=10):
    """
    Return recipes similar to a recipe.

    Intended for use on recipe_object page.
    """
    return []

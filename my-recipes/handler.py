import sys
import markdown

from flask import request, abort
from recipe_scrapers import scrape_me, WebsiteNotImplementedError
from slugify import slugify


class Recipe:
    '''Scrape a recipe from `gousto.co.uk` and convert it to markdown
    To be extended to other websites in the near future.'''
    def __init__(self, name, host='gousto.co.uk'):
        self.host = host
        self.recipe = self.scrape_recipe(name)

    def scrape_recipe(self, name):
        slug = slugify(name)
        url = 'https://' + self.host + '/' + 'cookbook' + '/' + 'recipes'
        recipe = dict()
        try:
            scraped_recipe = scrape_me(url + '/' + slug)
            instructions = [i for i in scraped_recipe.instructions(
                ).split('\n')]
            recipe = {
                    'title': scraped_recipe.title(),
                    'image': scraped_recipe.image(),
                    'serves': scraped_recipe.yields(),
                    'time': scraped_recipe.total_time(),
                    'ingredients': scraped_recipe.ingredients(),
                    'instructions': instructions
                    }
        except WebsiteNotImplementedError:
            pass

        return recipe

    def make_md(self):
        title = f"## {self.recipe['title']}"
        img = f"![Recipe picture]({self.recipe['image']})""{ width=50% }"
        time = f"Prep time: **{self.recipe['time']}** \
                [{self.recipe['serves']}]"
        ingr_t = '### Ingredients'
        ingr = "\n".join([f"- {i}" for i in self.recipe['ingredients']])
        instr_t = '### Instructions'
        instr = "\n".join([f"{num+1}. {item}"
                          for num, item in enumerate(
                              self.recipe['instructions'])])

        recipe = ""
        for i in [title, img, time, ingr_t, ingr, instr_t, instr]:
            recipe += f"{i}" + '\n\n'

        return recipe


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    # req = 'King Prawn Paella With Lemon Aioli'

    favourites = {
            "Aubergine Curry": "Thai Aubergine Curry With Sticky Rice",
            "Italian Burger": "Italian Vegan Burger With Olive & Basil Tapenade",
            "Prawn Paella": "King Prawn Paella With Lemon Aioli"
            }

    query = request.args.get('recipe')

    if not query:
        abort(404)

    try:
        choice = favourites.get(query.title(), "")
    except TimeoutError:
        raise Exception('Timeout trying to get request.')

    recipe = Recipe(choice)

    md = markdown.Markdown(extensions=[
        'markdown.extensions.meta',
        'markdown.extensions.tables',
        'markdown.extensions.extra',
        'markdown.extensions.nl2br',
        'markdown.extensions.smarty',
        'pymdownx.magiclink',
        'pymdownx.tasklist'
        ])

    return md.convert(recipe.make_md())

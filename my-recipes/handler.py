import markdown
import sys

from flask import request, Markup, render_template
from recipe_scrapers import scrape_me, WebsiteNotImplementedError
from slugify import slugify


favourites = {
        "1": "Thai Aubergine Curry With Sticky Rice",
        "2": "Italian Vegan Burger With Olive & Basil Tapenade",
        "3": "King Prawn Paella With Lemon Aioli",
        "4": "Smoked Mackerel Fishcakes & Apple Remoulade",
        "5": "Salmon & Sugar Snap Risotto",
        "6": "Butternut Squash, Lentil & Coconut Dal",
        "7": "Easy One-Pot Haddock & Leek Risotto",
        "8": "Warm Halloumi Salad With Green Tomato Dressing",
        "9": "10-Min Salmon With Spinach & Lemon Gnocchi",
        "10": "10-Min Spiced Lentil Stew & Chilli-Peanut Crumb",
        "11": "10-Min Spicy Halloumi Stew With Couscous",
        "12": "Mushroom & Thyme Fusilloni",
        "13": "10-Min Tomato & Goat's Cheese Gnocchi",
        "14": "Pistachio & Cranberry Nut Roast",
        "15": "10-Min Mushroom Biryani With Cucumber Raita",
        "16": "Burrata-Topped Tomato Risotto With Basil Oil",
        "17": " Saffron, Crab & Clotted Cream Risotto",
        "18": "Fragant Thai Crab Rice With Lime",
        "19": "Crispy Tofu, Satay Sauce & Sesame Rice",
        "20": "The Ultimate Veggie Cheeseburger & Tomato Relish"
        }


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
        img = f"![Recipe picture]({self.recipe['image']})""{ width=100% }"
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


def _parse_markdown(choice):
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


def handle(event, context):
    """handle a request to the function
    Args:
        req (str): request body
    """

    query = event.query.get('recipe')

    if not query:
        rendered = "<h2>Incomplete URL</h2>"
        status_code = 404
    elif query in favourites:
        choice = favourites.get(query.title(), "")
        rendered = Markup(_parse_markdown(choice))
        status_code = 200
    else:
        rendered = "<h2>Value no found</h2>"
        status_code = 404

    return {
            "statusCode": status_code,
            "body": rendered
            }

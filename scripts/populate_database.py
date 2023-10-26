import json

from recipe.models import Recipe


def run():
    file = 'C:/Users/Tsotne/Desktop/study/skillwill/skillwill_projects/recipes/scripts/mock_data.json'
    mock_data = open(file)
    data = json.load(mock_data)["data"]
    for recipe in data:
        Recipe.objects.create(**recipe)

from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Min, Max
from .models import Recipe, Category


def main(request):
    recipes = Recipe.objects.order_by('?')[:10]

    return render(request, 'main.html', {'recipes': recipes})


def category_detail(request, id):
    category = get_object_or_404(Category, id=id)

    recipes = Recipe.objects.filter(category=category)

    return render(request, 'category_detail.html', {'category': category, 'recipes': recipes})





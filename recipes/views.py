from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe, Favorite  # ← agregar Favorite aquí
from types import SimpleNamespace


def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    return render(request, "recipes/recipe_detail.html", {
        "recipe": recipe,
        "is_favorite": is_favorite,
    })


import re

def clean_steps(instructions):
    # Líneas a ignorar por patrón
    ignore_patterns = [
        r'^preparation steps',
        r'^the instructions',
        r'^instructions',
        r'^ingredients',
        r'^pro tip',
        r'^option [a-z]',
        r'^note[:\s]',
        r'^tip[:\s]',
    ]
    
    steps = []
    for line in instructions.split('\n'):
        line = line.strip()
        if not line:
            continue
        line_lower = line.lower()
        if any(re.match(p, line_lower) for p in ignore_patterns):
            continue
        # Ignorar líneas muy cortas (menos de 15 caracteres) que no son pasos reales
        if len(line) < 15:
            continue
        steps.append(line)
    
    return steps


def recipe_steps(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    steps = list(recipe.steps.all())  # Usar RecipeStep objects

    if not steps:
        parsed_steps = clean_steps(recipe.instructions)
        steps = [SimpleNamespace(description=text, image=None, step_number=i + 1, title=f"Step {i + 1}")
                 for i, text in enumerate(parsed_steps)]

    total = len(steps)
    display_total = total if total > 0 else 1
    try:
        current = int(request.GET.get('step', 1))
    except (TypeError, ValueError):
        current = 1
    current = max(1, min(current, display_total))
    step = steps[current - 1] if steps else SimpleNamespace(description="No hay pasos disponibles.", image=None, step_number=1, title="Step 1")

    return render(request, "recipes/recipe_steps.html", {
        "recipe": recipe,
        "step": step,
        "current": current,
        "total": display_total,
        "has_prev": current > 1,
        "has_next": current < total,
        "prev_num": current - 1,
        "next_num": current + 1,
    })


@login_required
def add_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    return redirect('recipes:recipe_detail', recipe_id)


@login_required
def remove_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    Favorite.objects.filter(user=request.user, recipe=recipe).delete()
    return redirect('recipes:my_favorites')


@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, "recipes/my_favorites.html", {"favorites": favorites})


def search(request):
    q = request.GET.get('q', '')
    results = Recipe.objects.filter(name__icontains=q) if q else Recipe.objects.none()
    return render(request, "recipes/search_results.html", {
        "q": q,
        "recipes": results,
    })
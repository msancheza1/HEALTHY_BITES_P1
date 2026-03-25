from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe, Favorite  # ← agregar Favorite aquí


def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    return render(request, "recipes/recipe_detail.html", {
        "recipe": recipe,
        "is_favorite": is_favorite,
    })


def recipe_steps(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    steps = [s.strip() for s in recipe.instructions.split('\n') if s.strip()]
    total = len(steps)
    current = int(request.GET.get('step', 1))
    current = max(1, min(current, total))
    return render(request, "recipes/recipe_steps.html", {
        "recipe": recipe,
        "step_text": steps[current - 1] if steps else "",
        "current": current,
        "total": total,
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
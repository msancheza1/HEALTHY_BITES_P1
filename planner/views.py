from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe, Favorite
from accounts.models import BMIRecord
from django.db.models import Q


def home(request):
    recipes = Recipe.objects.all()
    bmi = None

    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            bmi = profile.bmi()

            if profile.vegetarian:
                recipes = recipes.filter(vegetarian=True)
            if profile.diabetes:
                recipes = recipes.filter(diabetic_friendly=True)
            if profile.lactose_intolerant:
                recipes = recipes.filter(lactose_free=True)
            if profile.gluten_intolerant:
                recipes = recipes.filter(gluten_free=True)

            category = profile.bmi_category()
            if category == "overweight":
                recipes = recipes.filter(healthy=True)

        except:
            return redirect('profile')

    bmi_info = None
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            bmi_info = {
                'value': profile.bmi(),
                'category': profile.bmi_category(),
                'ideal_min': profile.ideal_weight_min(),
                'ideal_max': profile.ideal_weight_max(),
                'difference': profile.weight_difference(),
                'current_weight': profile.weight,
                'height_cm': int(profile.height * 100),
            }
        except:
            pass

    context = {
        'recipes': recipes,
        'bmi': bmi,
        'bmi_info': bmi_info,
    }
    return render(request, 'planner/home.html', context)


# FR16 — Vista paso a paso
# Lee las instructions línea por línea, no necesita datos extra en la BD
def recipe_steps(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    steps = [s.strip() for s in recipe.instructions.split('\n') if s.strip()]
    total = len(steps)

    try:
        current = int(request.GET.get('step', 1))
        current = max(1, min(current, total))
    except ValueError:
        current = 1

    context = {
        'recipe': recipe,
        'step_text': steps[current - 1] if steps else "No steps available.",
        'current': current,
        'total': total,
        'percent': int((current / total) * 100) if total > 0 else 0,
        'has_prev': current > 1,
        'has_next': current < total,
        'prev_num': current - 1,
        'next_num': current + 1,
    }
    return render(request, 'planner/recipe_steps.html', context)


# FR21 — Historial de progreso BMI
@login_required
def progress_history(request):
    records = BMIRecord.objects.filter(user=request.user).order_by('recorded_at')

    # Datos para la tabla (más reciente primero)
    records_desc = list(records.order_by('-recorded_at'))

    # Datos para el gráfico (cronológico)
    chart_labels = [r.recorded_at.strftime('%d %b %Y') for r in records]
    chart_bmi    = [r.bmi for r in records]
    chart_weight = [r.weight for r in records]

    context = {
        'records': records_desc,
        'chart_labels': chart_labels,
        'chart_bmi': chart_bmi,
        'chart_weight': chart_weight,
    }
    return render(request, 'planner/progress_history.html', context)


@login_required
def add_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    return redirect('home')


@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'recipes/my_favorites.html', {'favorites': favorites})


@login_required
def remove_favorite(request, recipe_id):
    Favorite.objects.filter(user=request.user, recipe_id=recipe_id).delete()
    return redirect('my_favorites')




def search(request):
    q = (request.GET.get("q") or "").strip()
    recipes = Recipe.objects.all()

    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            if profile.vegetarian:
                recipes = recipes.filter(vegetarian=True)
            if profile.diabetes:
                recipes = recipes.filter(diabetic_friendly=True)
            if profile.lactose_intolerant:
                recipes = recipes.filter(lactose_free=True)
            if profile.gluten_intolerant:
                recipes = recipes.filter(gluten_free=True)
            if profile.bmi_category() == "overweight":
                recipes = recipes.filter(healthy=True)
        except:
            return redirect('profile')

    if q:
        recipes = recipes.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(ingredients__icontains=q)
        )

    return render(request, "recipes/search_results.html", {"recipes": recipes, "q": q})
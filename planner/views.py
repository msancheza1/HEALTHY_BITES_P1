from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Recipe
from .forms import UserProfileForm


def home(request):
    recipes = Recipe.objects.all()
    bmi = None

    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            bmi = profile.bmi()

            # Filtro vegetariano
            if profile.vegetarian:
                recipes = recipes.filter(vegetarian=True)

            # Filtro diabetes
            if profile.diabetes:
                recipes = recipes.filter(diabetic_friendly=True)
            # filtro lactosa
            if profile.lactose_intolerant:
                recipes = recipes.filter(lactose_free=True)
            #filtro gluten
            if profile.gluten_intolerant:
                recipes = recipes.filter(gluten_free=True)
                
            #filtro por BMI
            category = profile.bmi_category()

            if category == "overweight":
                recipes = recipes.filter(healthy=True)

            elif category == "underweight":
                recipes = recipes  # puede ver todo

            elif category == "normal":
                recipes = recipes  # puede ver todo

        except:
            # Si no tiene perfil, lo enviamos a completarlo
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


@login_required
def profile_view(request):
    try:
        profile = request.user.userprofile
    except:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            return redirect('home')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'planner/profile.html', {'form': form})

from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'planner/register.html', {'form': form})

from django.shortcuts import get_object_or_404

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'planner/recipe_detail.html', {'recipe': recipe})

from .models import Favorite

@login_required
def add_favorite(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    return redirect('home')

@login_required
def my_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'planner/my_favorites.html', {'favorites': favorites})
## nueva funcion 

@login_required #debes estar logeado para poder acceder a esto
def remove_favorite(request, recipe_id):
    Favorite.objects.filter(user=request.user, recipe_id=recipe_id).delete()
    return redirect('my_favorites')
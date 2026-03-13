from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, BMIRecord
from .forms import UserProfileForm, RegisterForm


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

            # FR21 — Guardar snapshot del BMI cada vez que se actualiza el perfil
            BMIRecord.objects.create(
                user=request.user,
                weight=new_profile.weight,
                height=new_profile.height,
                bmi=new_profile.bmi(),
                category=new_profile.bmi_category(),
            )

            return redirect('home')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

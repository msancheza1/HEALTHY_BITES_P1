import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # ← cambia 'your_project' por el nombre de tu proyecto
django.setup()

from recipes.models import Recipe, RecipeStep

migrated = 0
skipped = 0

for recipe in Recipe.objects.all():
    # Si ya tiene pasos cargados, no los duplica
    if recipe.steps.exists():
        print(f"⏭️  Skipped (already has steps): {recipe.name}")
        skipped += 1
        continue

    # Divide instructions por salto de línea, igual que tu vista anterior
    lines = [s.strip() for s in recipe.instructions.split('\n') if s.strip()]

    if not lines:
        print(f"⚠️  No instructions found: {recipe.name}")
        skipped += 1
        continue

    for i, line in enumerate(lines, start=1):
        # Si la línea empieza con número (ej: "1. Hervir agua"), lo usa como título
        if line[0].isdigit() and '.' in line[:4]:
            parts = line.split('.', 1)
            title = f"Step {i}"
            description = parts[1].strip() if len(parts) > 1 else line
        else:
            title = f"Step {i}"
            description = line

        RecipeStep.objects.create(
            recipe=recipe,
            step_number=i,
            title=title,
            description=description,
        )

    print(f"✅ Migrated {len(lines)} steps: {recipe.name}")
    migrated += 1

print(f"\nDone. Migrated: {migrated} recipes | Skipped: {skipped}")
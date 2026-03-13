import sqlite3

db = r'c:\\Users\\User\\Documents\\PROYECTO P1\\HEALTHY_BITES_P1\\db.sqlite3'
conn = sqlite3.connect(db)
cur = conn.cursor()

cur.execute('SELECT count(*) FROM recipes_recipe')
recipes_count = cur.fetchone()[0]
cur.execute('SELECT count(*) FROM planner_recipe')
planner_count = cur.fetchone()[0]
print('Before migration recipes', recipes_count)
print('Before migration planner', planner_count)

if planner_count > 0 and recipes_count == 0:
    cur.execute('''
        INSERT INTO recipes_recipe
        (name, description, ingredients, instructions, image, vegetarian, diabetic_friendly, lactose_free, gluten_free, healthy)
        SELECT name, description, ingredients, instructions, image, vegetarian, diabetic_friendly, lactose_free, gluten_free, healthy
        FROM planner_recipe
    ''')
    conn.commit()
    print('Migration of recipes applied')

# migrate favorites by mapping names from old to new recipe IDs
cur.execute('SELECT id, name FROM planner_recipe')
planner_rows = cur.fetchall()
name_map = {rid: name for rid, name in planner_rows}
cur.execute('SELECT id, name FROM recipes_recipe')
recipe_rows = cur.fetchall()
name_to_new_id = {name: rid for rid, name in recipe_rows}

cur.execute('SELECT user_id, recipe_id FROM planner_favorite')
for user_id, planner_recipe_id in cur.fetchall():
    old_name = name_map.get(planner_recipe_id)
    if old_name:
        new_recipe_id = name_to_new_id.get(old_name)
        if new_recipe_id:
            cur.execute('INSERT OR IGNORE INTO recipes_favorite (user_id, recipe_id) VALUES (?, ?)', (user_id, new_recipe_id))
conn.commit()

cur.execute('SELECT count(*) FROM recipes_recipe')
print('After migration recipes', cur.fetchone()[0])
cur.execute('SELECT count(*) FROM recipes_favorite')
print('After migration favorites', cur.fetchone()[0])
conn.close()


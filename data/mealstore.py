import os
meal_list = []

def add_meal(name, image, cal, grams):
    meal_list.append({
        "name": name,
        "image": image,
        "cal": cal,
        "grams": grams
    })

def get_all_meals():
    return meal_list

def clear_meals():
    meal_list.clear()

def delete_meal(screen, meal_data):
    if meal_data in meal_list:
        path = meal_data.get('image')
        if path and os.path.isfile(path):
            os.remove(path)
        meal_list.remove(meal_data)
        if screen.name == "meal":
            screen.on_pre_enter()

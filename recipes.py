class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit
    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = float(value)
    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"
    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit
class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        if ingredients is None:
            self.ingredients = []
        else:
            self.ingredients = ingredients
    def add_ingredient(self, ingredient):
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)
    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0
    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Некорректный коэффициент")
        new_ingredients = []
        for ingredient in self.ingredients:
            new_ingredient = Ingredient(
                ingredient.name,
                ingredient.quantity * ratio,
                ingredient.unit
            )
            new_ingredients.append(new_ingredient)
        return Recipe(self.title, new_ingredients)
    def __len__(self):
        return len(self.ingredients)
    def __str__(self):
        result = self.title + "\n"
        for ingredient in self.ingredients:
            result += str(ingredient) + "\n"
        return result.strip()
class ShoppingList:
    def __init__(self):
        self._items = []
    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))
    def remove_recipe(self, title):
        new_items = []
        for item in self._items:
            if item[1] != title:
                new_items.append(item)
        self._items = new_items
    def get_list(self):
        ingredients_dict = {}
        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in ingredients_dict:
                ingredients_dict[key] += ingredient.quantity
            else:
                ingredients_dict[key] = ingredient.quantity
        result = []
        for key, quantity in ingredients_dict.items():
            name, unit = key
            result.append(Ingredient(name, quantity, unit))
        result.sort(key=lambda ingredient: ingredient.name)
        return result
    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list
class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type
    def scale(self, ratio):
        scaled_recipe = super().scale(ratio)
        return DietaryRecipe(
            scaled_recipe.title,
            self.diet_type,
            scaled_recipe.ingredients
        )
    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"
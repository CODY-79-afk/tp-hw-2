import pytest

from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


def test_ingredient_creation():
    ingredient = Ingredient("Мука", 500, "г")

    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")

    assert str(ingredient) == "Мука: 500.0 г"


def test_ingredient_equal():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 100, "г")

    assert ingredient1 == ingredient2


def test_ingredient_not_equal_name():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Сахар", 500, "г")

    assert ingredient1 != ingredient2


def test_ingredient_not_equal_unit():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 500, "кг")

    assert ingredient1 != ingredient2

def test_ingredient_negative_quantity():
    with pytest.raises(ValueError):
        Ingredient("Мука", -1, "г")


def test_recipe_creation():
    recipe = Recipe("Пицца")

    assert recipe.title == "Пицца"
    assert recipe.ingredients == []


def test_add_new_ingredient():
    recipe = Recipe("Пицца")

    recipe.add_ingredient(Ingredient("Мука", 500, "г"))

    assert len(recipe.ingredients) == 1


def test_add_duplicate_ingredient():
    recipe = Recipe("Пицца")

    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 700


def test_scale_returns_new_recipe():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])

    scaled = recipe.scale(2)

    assert scaled is not recipe


def test_scale_quantity():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])

    scaled = recipe.scale(2)

    assert scaled.ingredients[0].quantity == 1000


def test_scale_invalid_ratio():
    recipe = Recipe("Пицца")

    with pytest.raises(ValueError):
        recipe.scale(0)


def test_recipe_len():
    recipe = Recipe(
        "Пицца",
        [
            Ingredient("Мука", 500, "г"),
            Ingredient("Сыр", 200, "г")
        ]
    )

    assert len(recipe) == 2


def test_add_recipe():
    shopping = ShoppingList()

    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])

    shopping.add_recipe(recipe, 1)

    assert len(shopping._items) == 1


def test_add_recipe_invalid_portions():
    shopping = ShoppingList()
    recipe = Recipe("Пицца")

    with pytest.raises(ValueError):
        shopping.add_recipe(recipe, 0)


def test_remove_recipe():
    shopping = ShoppingList()

    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])

    shopping.add_recipe(recipe, 1)
    shopping.remove_recipe("Пицца")

    assert len(shopping._items) == 0


def test_remove_missing_recipe():
    shopping = ShoppingList()

    shopping.remove_recipe("Не существует")

    assert len(shopping._items) == 0


def test_get_list_sum():
    shopping = ShoppingList()

    recipe1 = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    recipe2 = Recipe("Хлеб", [Ingredient("Мука", 300, "г")])

    shopping.add_recipe(recipe1, 1)
    shopping.add_recipe(recipe2, 1)

    result = shopping.get_list()

    assert len(result) == 1
    assert result[0].quantity == 800


def test_get_list_sorted():
    shopping = ShoppingList()

    recipe = Recipe(
        "Пицца",
        [
            Ingredient("Яйца", 2, "шт"),
            Ingredient("Мука", 500, "г")
        ]
    )

    shopping.add_recipe(recipe, 1)

    result = shopping.get_list()

    assert result[0].name == "Мука"
    assert result[1].name == "Яйца"


def test_add_shopping_lists():
    shopping1 = ShoppingList()
    shopping2 = ShoppingList()

    recipe1 = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    recipe2 = Recipe("Хлеб", [Ingredient("Сахар", 100, "г")])

    shopping1.add_recipe(recipe1, 1)
    shopping2.add_recipe(recipe2, 1)

    merged = shopping1 + shopping2

    assert len(merged._items) == 2
    assert len(shopping1._items) == 1
    assert len(shopping2._items) == 1
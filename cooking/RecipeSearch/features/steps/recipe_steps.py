from behave import given, when, then
import uuid
import random

@given('I am on the homepage')
def step_impl(context):
    context.browser.visit(context.get_url('/'))

@given('I am registered as any user')
def step_impl(context):
    # Generate unique username and email for this scenario
    unique_id = str(uuid.uuid4())[:8]
    username = f"testuser_{unique_id}"
    email = f"{username}@example.com"
    password = "Z8$hsAKu2025"
    # Store for later steps
    context.username = username
    context.email = email
    context.password = password
    context.browser.visit(context.get_url('/register/'))
    context.browser.fill('username', username)
    context.browser.fill('email', email)
    context.browser.fill('password1', password)
    context.browser.fill('password2', password)
    context.browser.find_by_css('button[type="submit"]').click()
    print("REGISTRATION PAGE HTML:\n", context.browser.html)
    assert not context.browser.is_text_present("Registration failed")

@given('I am logged in as that user')
def step_impl(context):
    context.browser.visit(context.get_url('/login/'))
    context.browser.fill('username', context.username)
    context.browser.fill('password', context.password)
    context.browser.find_by_css('button[type="submit"]').click()
    print("LOGIN PAGE HTML:\n", context.browser.html)
    assert not context.browser.is_text_present("Login")
    
@given('there is a recipe titled "{title}"')
def step_impl(context, title):
    from recipes.models import Recipe, Category
    category, _ = Category.objects.get_or_create(name='Test Category')
    spoonacular_id = random.randint(10000, 99999)
    recipe = Recipe.objects.create(
        title=title,
        spoonacular_id=spoonacular_id,
        category=category,
        instructions='Test instructions'
    )
    context.recipe_spoonacular_id = recipe.spoonacular_id

@when('I visit the recipes page')
def step_impl(context):
    context.browser.visit(context.get_url('/recipes/'))

@when('I enter "{text}" in the search box')
def step_impl(context, text):
    context.browser.fill('search', text)

@when('I click the search button')
def step_impl(context):
    context.browser.find_by_css('button[type="submit"]').click()

@when('I click on the recipe "{title}"')
def step_impl(context, title):
    context.browser.visit(context.get_url(f'/recipe/{context.recipe_spoonacular_id}/'))

@when('I click the "{button_text}" button')
def step_impl(context, button_text):
    print("CLICK BUTTON PAGE HTML:\n", context.browser.html)
    try:
        context.browser.find_by_text(button_text).first.click()
    except Exception:
        # Fallback: try by CSS class if text fails
        context.browser.find_by_css('.btn-custom').first.click()

@when('I enter "{text}" in the feedback form')
def step_impl(context, text):
    print("FEEDBACK FORM PAGE HTML:\n", context.browser.html)
    context.browser.fill('comment', text)

@when('I submit the feedback')
def step_impl(context):
    context.browser.find_by_value('Submit Feedback').click()

@then('I should see a list of recipes')
def step_impl(context):
    assert context.browser.is_text_present('Recipes')

@then('I should see recipes containing "{text}"')
def step_impl(context, text):
    assert context.browser.is_text_present(text)

@then('I should see the recipe details')
def step_impl(context):
    assert context.browser.is_text_present('Ingredients')
    assert context.browser.is_text_present('Instructions')

@then('I should see the ingredients list')
def step_impl(context):
    assert context.browser.is_text_present('Ingredients')

@then('I should see the cooking instructions')
def step_impl(context):
    assert context.browser.is_text_present('Instructions')

@then('I should see a success message')
def step_impl(context):
    assert context.browser.is_text_present('Recipe saved successfully')

@then('the recipe should be in my saved recipes')
def step_impl(context):
    from recipes.models import SavedRecipe
    assert SavedRecipe.objects.filter(user__username='testuser').exists()

@then('I should see my feedback displayed')
def step_impl(context):
    assert context.browser.is_text_present('This is a great recipe!')

@given('I am viewing a recipe')
def step_impl(context):
    from recipes.models import Recipe
    recipe = Recipe.objects.first()
    context.recipe_id = recipe.id
    context.browser.visit(context.get_url(f'/recipe/{recipe.id}/')) 
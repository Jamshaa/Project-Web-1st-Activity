Feature: Recipe Management
    As a user
    I want to manage recipes
    So that I can organize my cooking experience

    Background:
        Given I am registered as any user
        And there is a recipe titled "Spaghetti Carbonara"

    Scenario: View recipe list
        When I visit the recipes page
        Then I should see a list of recipes

    Scenario: Search for a recipe
        When I visit the recipes page
        And I enter "Spaghetti" in the search box
        And I click the search button
        Then I should see recipes containing "Spaghetti"

    Scenario: View recipe details
        Given I am registered as any user
        And there is a recipe titled "Spaghetti Carbonara"
        When I click on the recipe "Spaghetti Carbonara"
        Then I should see the recipe details
        And I should see the ingredients list
        And I should see the cooking instructions

    Scenario: Save a recipe
        Given I am registered as any user
        And there is a recipe titled "Spaghetti Carbonara"
        When I click on the recipe "Spaghetti Carbonara"
        And I click the "Save Recipe" button
        Then I should see a success message
        And the recipe should be in my saved recipes

    Scenario: Add recipe feedback
        Given I am registered as any user
        And there is a recipe titled "Spaghetti Carbonara"
        When I click on the recipe "Spaghetti Carbonara"
        And I enter "This is a great recipe!" in the feedback form
        And I submit the feedback
        Then I should see my feedback displayed 
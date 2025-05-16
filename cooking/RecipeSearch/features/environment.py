from django.core.management import call_command
from django.test.runner import DiscoverRunner
from django.test.testcases import LiveServerTestCase
from splinter import Browser
import os
import django

def before_all(context):
    django.setup()
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()
    context.browser = Browser('chrome', headless=True)

    # Add this helper for building URLs
    def get_url(path):
        # Default test server address
        return f'http://localhost:8000{path}'
    context.get_url = get_url

def after_all(context):
    context.browser.quit()
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()

def before_scenario(context, scenario):
    call_command('flush', verbosity=0, interactive=False)

def after_scenario(context, scenario):
    pass 
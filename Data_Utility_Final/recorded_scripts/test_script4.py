# This is a sample script for demonstration
import random


def sample_function():
    page.locator('#username').fill('testuser')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.get_by_label('Account').fill('Savings')
    page.fill('#amount', random.randint(1, 1000))

    # Perform some other actions
    page.locator('#submit').click()

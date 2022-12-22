import random
from uuid import uuid4

import allure
import pytest

from config import ADMIN_PANEL_CREDENTIALS


@allure.title("Checking the visibility of elements on the admin panel login page")
def test_admin_panel_login_page_elements_visibility(driver):
    login_page(driver) \
        .open_page() \
        .check_for_visible_elements()


@allure.title("Adding new product in admin panel")
def test_adding_new_product_in_admin_panel(driver):
    actual_success_message = login_page(driver) \
        .open_page() \
        .login(*ADMIN_PANEL_CREDENTIALS) \
        .click_to_menu_catalog() \
        .click_to_menu_catalog_products() \
        .click_to_add_product() \
        .fill_in_name(str(uuid4())) \
        .fill_in_meta_tag_title(str(uuid4())) \
        .click_to_data_tab() \
        .fill_in_model(str(uuid4())) \
        .fill_in_price(random.randint(1, 100)) \
        .click_to_save() \
        .get_success_message()
    assert "Success: You have modified products!" in actual_success_message


@allure.title("Removing product from list in admin panel")
def test_removing_product_from_list_in_admin_panel(driver):
    actual_success_message = login_page(driver) \
        .open_page() \
        .login(*ADMIN_PANEL_CREDENTIALS) \
        .click_to_menu_catalog() \
        .click_to_menu_catalog_products() \
        .product_card_list.select_by_index(0) \
        .click_to_delete_product() \
        .accept_delete() \
        .get_success_message()
    assert "Success: You have modified products!" in actual_success_message


@pytest.mark.parametrize("currency", ["$", "€", "£"])
def test_switch_currency(driver, currency):
    main_page = MainPage(driver) \
        .open_page() \
        .open_currency_dropdown() \
        .select_currency_by_symbol(currency)
    assert main_page.is_present_currency(currency)
    assert main_page.get_visible_current_currency() == currency
    assert main_page.product_card_list.get_product_price_by_index(0).find(currency) >= 0


@pytest.mark.smoke
@allure.title("Checking the visibility of elements on the register page")
def test_register_page_elements_visibility(driver):
    MainPage(driver) \
        .open_page() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .check_for_visible_elements()


@pytest.mark.smoke
@allure.title("Registering a new user")
def test_registering_new_user(driver):
    person = correct_random_person()
    register_success_page = MainPage(driver) \
        .open_page() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .register_person(person) \
        .wait_for_page_load()
    assert register_success_page.get_success_header_text() == "Your Account Has Been Created!"


@allure.title("Attempt to register an existing user")
def test_registering_existing_user(driver):
    person = correct_random_person()
    register_page = MainPage(driver) \
        .open_page() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .register_person(person) \
        .wait_for_page_load() \
        .open_my_account_dropdown() \
        .logout() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .try_to_register_person(person)
    assert register_page.get_header_text() == "Register Account"
    assert register_page.get_alert_danger_text() == "Warning: E-Mail Address is already registered!"


@allure.title("Registration attempt with a non-accepted privacy policy")
def test_registering_non_accepted_privacy_policy(driver):
    person = correct_random_person()
    register_page = MainPage(driver) \
        .open_page() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .fill_all_personal_fields(person) \
        .try_to_continue()
    assert register_page.get_header_text() == "Register Account"
    assert register_page.get_alert_danger_text() == "Warning: You must agree to the Privacy Policy!"


@allure.title("Attempt to register with an empty firstname")
def test_registering_empty_firstname(driver):
    person = person_with_empty_firstname()
    register_page = MainPage(driver) \
        .open_page() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .try_to_register_person(person)
    assert register_page.get_header_text() == "Register Account"
    assert register_page.get_firstname_danger_text() == "First Name must be between 1 and 32 characters!"


@allure.title("Attempt to register with an empty lastname")
def test_registering_empty_lastname(driver):
    person = person_with_empty_lastname()
    register_page = MainPage(driver) \
        .open_page() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .try_to_register_person(person)
    assert register_page.get_header_text() == "Register Account"
    assert register_page.get_lastname_danger_text() == "Last Name must be between 1 and 32 characters!"


@allure.title("Attempt to register with an empty email")
def test_registering_empty_email(driver):
    person = person_with_empty_email()
    register_page = MainPage(driver) \
        .open_page() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .try_to_register_person(person)
    assert register_page.get_header_text() == "Register Account"
    assert register_page.get_email_danger_text() == "E-Mail Address does not appear to be valid!"


@allure.title("Attempt to register with an empty telephone")
def test_registering_empty_telephone(driver):
    person = person_with_empty_telephone()
    register_page = MainPage(driver) \
        .open_page() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .try_to_register_person(person)
    assert register_page.get_header_text() == "Register Account"
    assert register_page.get_telephone_danger_text() == "Telephone must be between 3 and 32 characters!"


@allure.title("Attempt to register with an empty password")
def test_registering_empty_password(driver):
    person = person_with_empty_password()
    register_page = MainPage(driver) \
        .open_page() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .try_to_register_person(person)
    assert register_page.get_header_text() == "Register Account"
    assert register_page.get_password_danger_text() == "Password must be between 4 and 20 characters!"


@allure.title("Attempt to register with an empty confirm")
def test_registering_empty_password_confirm(driver):
    person = person_with_empty_password_confirm()
    register_page = MainPage(driver) \
        .open_page() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .try_to_register_person(person)
    assert register_page.get_header_text() == "Register Account"
    assert register_page.get_password_confirm_danger_text() == "Password confirmation does not match password!"


@allure.title("Attempt to register with different passwords")
def test_registering_different_passwords(driver):
    person = person_with_different_passwords()
    register_page = MainPage(driver) \
        .open_page() \
        .open_my_account_dropdown() \
        .open_register_page() \
        .try_to_register_person(person)
    assert register_page.get_header_text() == "Register Account"
    assert register_page.get_password_confirm_danger_text() == "Password confirmation does not match password!"
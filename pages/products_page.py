import allure
from selenium.webdriver.common.by import By

from page_objects.admin_panel.add_product_page import AddProductPage
from page_objects.base_page_object import BasePageObject


class ProductsPage(BasePageObject):
    _LOCATOR_ADD_PRODUCT_BUTTON = (By.CSS_SELECTOR, "a[data-original-title='Add New']")
    _LOCATOR_DELETE_PRODUCT_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Delete']")
    _LOCATOR_SUCCESS_ALERT = (By.CSS_SELECTOR, "div.alert.alert-success.alert-dismissible")

    def __init__(self, driver):
        super().__init__(driver)
        from page_objects.admin_panel.product_rows import ProductRows
        self.product_card_list = ProductRows(driver)

    @allure.step
    def click_to_add_product(self) -> AddProductPage:
        self.click(self._LOCATOR_ADD_PRODUCT_BUTTON)
        return AddProductPage(self.driver)

    @allure.step
    def click_to_delete_product(self):
        self.click(self._LOCATOR_DELETE_PRODUCT_BUTTON)
        return self

    @allure.step
    def accept_delete(self):
        self.present_alert().accept()
        return self

    @allure.step
    def cancel_delete(self):
        self.present_alert().dismiss()
        return self

    @allure.step
    def get_success_message(self) -> str:
        return self.visible_element(self._LOCATOR_SUCCESS_ALERT).text
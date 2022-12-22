import allure
from selenium.webdriver.common.by import By

from page_objects.admin_panel.products_page import ProductsPage
from page_objects.base_page_object import BasePageObject


class ProductRows(BasePageObject):
    _LOCATOR_PRODUCT_ROWS = (By.CSS_SELECTOR, "#form-product >* table > tbody > tr")
    _LOCATOR_PRODUCT_ROW_CHECKBOX = (By.CSS_SELECTOR, "#form-product >* table >tbody> tr > td > input[type='checkbox']")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step
    def select_by_index(self, index: int) -> ProductsPage:
        self.visible_elements(self._LOCATOR_PRODUCT_ROWS)[index] \
            .find_element(*self._LOCATOR_PRODUCT_ROW_CHECKBOX) \
            .click()
        return ProductsPage(self.driver)
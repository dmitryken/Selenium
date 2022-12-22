import allure
from selenium.webdriver.common.by import By

from page_objects.admin_panel.products_page import ProductsPage
from page_objects.base_page_object import BasePageObject


class MainPage(BasePageObject):
    _LOCATOR_MENU_CATALOG = (By.CSS_SELECTOR, "#menu-catalog")
    _LOCATOR_MENU_CATALOG_PRODUCTS = (By.LINK_TEXT, "Products")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step
    def click_to_menu_catalog(self):
        self.click(self._LOCATOR_MENU_CATALOG)
        return self

    @allure.step
    def click_to_menu_catalog_products(self) -> ProductsPage:
        self.click(self._LOCATOR_MENU_CATALOG_PRODUCTS)
        return ProductsPage(self.driver)
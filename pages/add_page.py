import allure
from selenium.webdriver.common.by import By

from page_objects.base_page_object import BasePageObject


class AddProductPage(BasePageObject):
    _LOCATOR_NAME_LOCATOR = (By.CSS_SELECTOR, "#form-product > * #input-name1")
    _LOCATOR_META_TAG_TITLE = (By.CSS_SELECTOR, "#form-product > * #input-meta-title1")
    _LOCATOR_MODEL = (By.CSS_SELECTOR, "#form-product > * #input-model")
    _LOCATOR_PRICE = (By.CSS_SELECTOR, "#form-product > * #input-price")
    _LOCATOR_SAVE_BUTTON_ = (By.CSS_SELECTOR, "button[data-original-title='Save']")
    _LOCATOR_DATA_TAB = (By.LINK_TEXT, 'Data')

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step
    def fill_in_name(self, value):
        self.input(self._LOCATOR_NAME_LOCATOR, value)
        return self

    @allure.step
    def fill_in_meta_tag_title(self, value):
        self.input(self._LOCATOR_META_TAG_TITLE, value)
        return self

    @allure.step
    def fill_in_model(self, value):
        self.input(self._LOCATOR_MODEL, value)
        return self

    @allure.step
    def fill_in_price(self, value):
        self.input(self._LOCATOR_PRICE, value)
        return self

    @allure.step
    def click_to_data_tab(self):
        self.click(self._LOCATOR_DATA_TAB)
        return self

    @allure.step
    def click_to_save(self):
        self.click(self._LOCATOR_SAVE_BUTTON_)
        from page_objects.admin_panel.products_page import ProductsPage
        return ProductsPage(self.driver)
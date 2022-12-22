import os

import allure
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver

from config import (
    DEFAULT_BROWSER,
    DEFAULT_OPENCART_BASE_URL,
    DEFAULT_SELENIUM_DRIVERS_PATH,
    DEFAULT_HEADLESS_MODE,
    DEFAULT_EXECUTOR,
    DEFAULT_SELENOID_BROWSER_VERSION,
    DEFAULT_LOGGING_LEVEL
)


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default=DEFAULT_BROWSER,
        choices=["chrome", "firefox", "opera"],
        help="possible values: chrome, firefox opera"
    )
    parser.addoption(
        "--url",
        default=DEFAULT_OPENCART_BASE_URL,
        help="opencart application address"
    )
    parser.addoption(
        "--drivers",
        default=os.path.expanduser(DEFAULT_SELENIUM_DRIVERS_PATH),
        help="the path to directory with Selenium drivers"
    )
    parser.addoption(
        "--headless",
        type=bool,
        default=DEFAULT_HEADLESS_MODE,
        help="headless mode, bool type. Default False.")
    parser.addoption(
        "--executor",
        default=DEFAULT_EXECUTOR,
        help="if executor!=local - autotests will run remotely in selenoid"
    )
    parser.addoption(
        "--browser_version",
        default=DEFAULT_SELENOID_BROWSER_VERSION,
        help="browser version for selenoid browser"
    )


@pytest.fixture()
def driver(request) -> WebDriver:
    browser = request.config.getoption("--browser")
    drivers_path = request.config.getoption("--drivers")
    base_url = request.config.getoption("--url")
    headless_mode = request.config.getoption("--headless")
    executor = request.config.getoption("--executor")
    browser_version = request.config.getoption("--browser_version")

    if executor == "local":
        if browser == "chrome":
            service = ChromeService(executable_path=drivers_path + "chromedriver")
            options = webdriver.ChromeOptions()
            if headless_mode:
                options.headless = True
            driver = webdriver.Chrome(service=service, options=options)
        elif browser == "firefox":
            service = FirefoxService(executable_path=drivers_path + "geckodriver")
            options = webdriver.FirefoxOptions()
            if headless_mode:
                options.headless = True
            driver = webdriver.Firefox(service=service, options=options)
        elif browser == "opera":
            service = ChromeService(executable_path=drivers_path + "operadriver")
            options = webdriver.ChromeOptions()
            if headless_mode:
                options.headless = True
            driver = webdriver.Chrome(service=service, options=options)
        else:
            raise ValueError(f"Browser {browser} is not supported.")
    else:
        executor_url = f"http://{executor}:4444/wd/hub"
        capabilities = {
            "browserName": browser,
            "browserVersion": browser_version,
            "name": "gulf98",
            "selenoid:options": {
                "enableVNC": False,
                "enableVideo": False,
                "enableLog": True
            },
            "acceptSslCerts": True,
            "acceptInsecureCerts": True,
            "timeZone": "Europe/Moscow"
        }
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=capabilities)

    def finalizer():
        if request.node.result != "passed":
            allure.attach(
                body=driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        driver.close()

    request.addfinalizer(finalizer)

    driver.log_level = DEFAULT_LOGGING_LEVEL
    driver.test_name = request.node.name

    driver.maximize_window()
    driver.base_url = base_url
    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        item.result = result.outcome
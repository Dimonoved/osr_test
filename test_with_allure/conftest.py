from sys import platform
from pathlib import Path
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="class")
@allure.title("Подготовка к тестам, активируем/деактивируем драйвер")
def browser(request):
    """
    возвращает экземпляр драйвера с заданными параметрами
    """
    chrome_options = webdriver.ChromeOptions()
    download_path = str(Path('.').absolute())
    prefs = {'download.default_directory': download_path,
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "safebrowsing.enabled": True
             }
    chrome_options.add_experimental_option('prefs', prefs)
    config = request.config.inicfg
    executable_path = config['executable_path']
    if executable_path:
        service = Service(executable_path=str(Path(executable_path).absolute()))
    else:
        service = Service()

    browser = webdriver.Chrome(service=service, options=chrome_options)
    yield browser
    browser.close()
    browser.quit()


@pytest.fixture()
@allure.title("Подготовка к тестам, определяем ОС")
def os_name():
    """
    возвращает название ос в соответствии с параметрами системы
    """
    os = {"windows": "Windows",
          "linux": "Linux",
          "linux2": "Linux",
          "win32": "Windows",
          "cygwin": "Windows",
          "msys": "Windows",
          "darwin": "MacOS"}
    return os[platform]


@pytest.fixture
@allure.title("Подготовка к тестам, получаем данные для тестов")
def options(request):
    """
    возвращает словарь с данными для теста
    """
    config = request.config.inicfg
    return config

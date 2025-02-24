from time import sleep
from pathlib import Path
import allure
from pages.sbis import Sbis


@allure.suite("Тест 3: проверяем локальные  загрузки")
@allure.sub_suite("Тест 3: проверяем загрузку веб-установщика сбис-плагина")
class TestPluginDownload:
    """
    Тестируем загрузку файла веб-установщика сбис плагина в соответствии версией ОС
    """

    @allure.title(
        "Тест 3.1: проверяем переход в раздел загрузок и скачивание веб-установщика сбис-плагина для выбранной ОС")
    def test_plugin_download(self, browser, os_name, options):
        """
        Переходим с продуктового сайта в раздел загрузок локальных версии.
        Выбираем сбис-плагин и скачиваем веб-установщик в соответствии ОС.
        По окончанию загрузки проверяем размер скаченного файла.
        Удаляем файл по завершению теста.
        """
        with allure.step("На продуктовом саите переходим в раздел локальных загрузок"):
            user = Sbis(browser, options['delay'])
            user.get(options['url_sbis'])
            user.goto_download_local()
        with allure.step("В разделе загрузок выбираем раздел плагина и требуемую ОС"):
            user.plugin_section_selected()
            user.os_section_selected(os_name)
            url_plugin, size = user.get_plugin_link(os_name)
        with allure.step("скачиваем веб-установщик сбис-плагина"):
            file_name = Path(f"{url_plugin.split('/')[-1]}")
            user.get(url_plugin)
            while not file_name.is_file():
                sleep(0.5)
        info = file_name.stat()
        file_name.unlink()
        assert size == round(info.st_size / 1048576, 2), "размер файла не верен"

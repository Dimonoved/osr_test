from time import sleep
from pathlib import Path
from pages.sbis import Sbis


class TestPluginDownload:
    """
    Тестируем загрузку файла веб-установщика сбис плагина в соответствии версией ОС
    """

    def test_plugin_download(self, browser, os_name, options):
        """
        Переходим с продуктового сайта в раздел загрузок локальных версии.
        Выбираем сбис-плагин и скачиваем веб-установщик в соответствии ОС.
        По окончанию загрузки проверяем размер скаченного файла.
        Удаляем файл по завершению теста.
        """
        browser.get(options['url_sbis'])
        user = Sbis(browser, options['delay'])
        user.goto_download_local()
        user.plugin_section_selected()
        user.os_section_selected(os_name)
        url_plugin, size = user.get_plugin_link(os_name)
        file_name = Path(f"{url_plugin.split('/')[-1]}")
        user.driver.get(url_plugin)
        while not file_name.is_file():
            sleep(0.5)
        info = file_name.stat()
        file_name.unlink()
        assert size == round(info.st_size / 1048576, 2), "размер файла не верен"

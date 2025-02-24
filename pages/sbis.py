from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Sbis:
    """
    Класс для работы с элементами на Sbis.ru
    """
    contacts_menu = (By.CSS_SELECTOR, "div.sbisru-Header-ContactsMenu")
    contacts_page = (By.CSS_SELECTOR, "div.sbisru-Header-ContactsMenu a.sbisru-link")
    contact_tensor = (By.CSS_SELECTOR, "div#contacts_clients a[title='tensor.ru']")
    region_name_selected = (By.CSS_SELECTOR, ".sbisru-Contacts__relative .sbis_ru-Region-Chooser")
    region_partner_list = (By.CSS_SELECTOR, "div#contacts_list div[data-qa='list']")
    region_menu_list = (By.CSS_SELECTOR, "div[name='dialog'] li")
    footer_download_local_versions = (
        By.XPATH, "//div[contains(@class, 'sbisru-Footer')]//a[contains(text(),'Скачать локальные версии')]")
    plugin_section = (By.CSS_SELECTOR, "div[data-component='SBIS3.CONTROLS/Tab/Buttons'] div[data-id='plugin']")
    os_section = (By.CSS_SELECTOR, "div[data-component='SBIS3.CONTROLS/Tab/Buttons'] div[data-id]")
    os_menu = (By.CSS_SELECTOR, "div.sbis_ru-DownloadNew-tabs__item")
    download_links_linux = (By.CSS_SELECTOR, "div[data-for ='linux'] ol a.sbis_ru-DownloadNew-loadLink")
    download_links_windows = (By.CSS_SELECTOR, "div[data-for ='default'] a.sbis_ru-DownloadNew-loadLink__link")
    download_links_macos = (By.CSS_SELECTOR, "div[data-for ='macos'] a.sbis_ru-DownloadNew-loadLink__link")

    def __init__(self, driver, delay):
        self.driver = driver
        self.delay = delay
        self.WebDriverWait = WebDriverWait(self.driver, self.delay)

    def get(self, url):
        """
        открытие ресурса методом get
        """
        self.driver.get(url)

    def open_contacts_menu(self):
        """
        открытие меню контактов
        """
        self.WebDriverWait.until(EC.visibility_of_element_located(self.contacts_menu))
        self.WebDriverWait.until(EC.element_to_be_clickable(self.contacts_menu)).click()

    def goto_contacts_page(self):
        """
        переход на страницу контактов
        """
        self.WebDriverWait.until(EC.visibility_of_element_located(self.contacts_page))
        self.WebDriverWait.until(EC.element_to_be_clickable(self.contacts_page)).click()

    def get_region_name(self):
        """
        получаем название выбранного региона
        """
        self.WebDriverWait.until(EC.visibility_of_element_located(self.region_name_selected))
        name = self.WebDriverWait.until(EC.presence_of_element_located(self.region_name_selected)).text
        return name

    def choice_region_menu(self, text):
        """
        открываем меню выбора региона и возвращает ссылку на целевой регион по названию
        :param text: название региона
        """
        self.WebDriverWait.until(EC.element_to_be_clickable(self.region_name_selected)).click()
        regions = self.WebDriverWait.until(EC.visibility_of_all_elements_located(self.region_menu_list))
        for region in regions:
            if text in region.text:
                region.click()
                self.WebDriverWait.until(EC.invisibility_of_element(self.region_menu_list))
                sleep(1)
                return

    def get_partners(self):
        """
        Возвращает список партнеров в разделе контактов в виде текста
        """
        self.WebDriverWait.until(EC.visibility_of_element_located(self.region_partner_list))
        return self.WebDriverWait.until(EC.presence_of_element_located(self.region_partner_list)).text

    def get_page_title(self):
        """
        возвращает текст заголовка страницы
        """
        return self.driver.title

    def get_current_url(self):
        """
         возвращает текущий url
         """
        return self.driver.current_url

    def goto_tensor(self):
        """
         переходит по банеру Тензора в разделе контактов
         """
        self.WebDriverWait.until(EC.visibility_of_element_located(self.contact_tensor))
        self.WebDriverWait.until(EC.element_to_be_clickable(self.contact_tensor)).click()

    def goto_download_local(self):
        """
        С продуктового сайта переходим в раздел локальных загрузок
        """
        self.WebDriverWait.until(EC.visibility_of_element_located(self.footer_download_local_versions))
        self.WebDriverWait.until(EC.element_to_be_clickable(self.footer_download_local_versions)).click()

    def plugin_section_selected(self):
        """
        выбираем в левом меню раздел плагина
        """
        self.WebDriverWait.until(EC.visibility_of_element_located(self.plugin_section))
        self.WebDriverWait.until(EC.element_to_be_clickable(self.plugin_section)).click()

    def os_section_selected(self, os_name):
        """
        выбираем в меню ОС
        :param os_name: название ОС
        """
        menu = self.WebDriverWait.until(EC.visibility_of_element_located(self.os_menu))
        section_os = WebDriverWait(menu, self.delay).until(EC.visibility_of_all_elements_located(self.os_section))
        for section in section_os:
            if section.text == os_name:
                section.click()
                return

    def get_plugin_link(self, os_name):
        """
        получаем ссылку на веб-установщик сбис-плагина
        :param os_name: название ОС
        :return: ссылка на плагин, размер файла
        """

        if os_name == "MacOS":
            links = self.WebDriverWait.until(EC.element_to_be_clickable(self.download_links_macos))
            size = float(links.text.split()[-2])
        elif os_name == "Linux":
            links = self.WebDriverWait.until(EC.element_to_be_clickable(self.download_links_linux))
            size = 0.02
            # для ОС linux размер файла на сайте отсутствует, размер установлен исходя из фактического
        else:
            links = self.WebDriverWait.until(EC.element_to_be_clickable(self.download_links_windows))
            size = float(links.text.split()[-2])

        return links.get_attribute('href'), size

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Tensor:
    """
    Класс для работы с элементами на Tensor.ru
    """

    block_link = (By.XPATH, "//p/text()[.='Сила в людях']/../..//a[contains(text(),'Подробнее')]")
    news_block_title = (By.CSS_SELECTOR, "div.tensor_ru-section  p.tensor_ru-Index__card-title")
    work_block_by_text_img = (
        By.XPATH, "//div[contains(@class,'tensor_ru-section')]//*[contains(text(),'Работаем')]/../..//img")

    def __init__(self, driver, delay):
        self.driver = driver
        self.delay = delay
        self.WebDriverWait = WebDriverWait(self.driver, self.delay)

    def get(self, url):
        """
        открытие ресурса методом get
        """
        self.driver.get(url)

    def current_url (self):
        """
        возвращает текущий url
        """
        return self.driver.current_url

    def check_text_in_news(self, text):
        """
        Проверяем заголовок карточки инфо-блока на соответствие целевому тексту
        :param text: целевой текст
        """
        self.WebDriverWait.until(EC.visibility_of_element_located(self.news_block_title))
        news_block = self.WebDriverWait.until(EC.presence_of_all_elements_located(self.news_block_title))
        for block in news_block:
            if text in block.text:
                return True

    def goto_block_link(self):
        """
        переходим по ссылке с текстом Подробнее из карточки инфо-блока

        """
        self.WebDriverWait.until(EC.visibility_of_element_located(self.block_link))
        self.WebDriverWait.until(EC.element_to_be_clickable(self.block_link)).click()

    def get_img_size(self):
        """
        получаем размеры картинок инфо-блока
        :return: список кортежей размеров картинок (длина, высота)
        """
        all_img = self.WebDriverWait.until(EC.presence_of_all_elements_located(self.work_block_by_text_img))
        all_img_size = []
        for img in all_img:
            all_img_size.append((img.get_attribute("width"), img.get_attribute("height")))
        return all_img_size

from pages.sbis import Sbis
from pages.tensor import Tensor


class TestInfoBlock:
    """
    Тестируем переход из карточки блока в инфо-блок и верстку фотографии в инфо-блоке.
    """

    def test_info_block(self, browser, options):
        """
        Тест переходит с продуктового сайта на сайт компании.
        Проверяем наличие карточки инфо-блока с заголовком 'Сила в людях'.
        Проверяет корректный перехода из карточки в инфо-блок.
        Проверяем верстку фотографии в инфо-блоке.
        """
        user = Sbis(browser, options['delay'])
        user.get(options['url_sbis'])
        user.open_contacts_menu()
        user.goto_contacts_page()
        user.goto_tensor()
        user.driver.switch_to.window(user.driver.window_handles[1])
        user = Tensor(browser, options['delay'])
        assert user.check_text_in_news(options['news_text']), f"нет инфо-банера с заголовком {options['news_text']}"
        user.goto_block_link()
        assert user.current_url() == options['url_tensor_about'], "ссылка из карточки ведет не в инфо-блок"
        images_size = user.get_img_size()
        for img in images_size[1:]:
            assert images_size[0] == img, "картинки в инфо-блоке разного размера"

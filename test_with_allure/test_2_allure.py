import allure
from pages.sbis import Sbis


@allure.suite("Тест 2: проверка раздела контактов продуктового сайта")
@allure.sub_suite("Тест 2: проверка формирования раздела контактов в зависимости от выбранного региона")
class TestRegionContacts:
    """
    Проверяет корректность формирования раздела контактов для региона по умолчанию и при выборе целевого региона
    """

    @allure.title("Тест 2.1: проверка раздела контактов для региона по умолчанию")
    def test_default_region_contacts(self, browser, options):
        """
        Тестируем формирование раздела контактов для региона по умолчанию
        """
        with allure.step("На продуктовом саите переходим в раздел контактов"):
            user = Sbis(browser, options['delay'])
            user.get(options['url_sbis'])
            user.open_contacts_menu()
            user.goto_contacts_page()
        with allure.step("Проверяем раздел контактов для региона по умолчанию"):
            assert options[
                       'region_local'] == user.get_region_name(), f"регион по умолчанию не {options['region_local']}"
            assert user.get_partners(), "список партнеров отсутствует"

    @allure.title("Тест 2.2: проверка изменения информации в разделе контактов для целевого региона")
    def test_region_change(self, browser, options):
        """
        Проверяем корректность формирование раздела контактов при изменении региона по умолчанию на целевой регион
        """
        with allure.step("Изменяем регион в разделе контактов"):
            user = Sbis(browser, options['delay'])
            partner_current = user.get_partners()
            user.choice_region_menu(options['region_remote'])
        with allure.step("Проверяем соответствие информации для целевого региона"):
            partner_new = user.get_partners()
            assert options[
                       'region_remote'] == user.get_region_name(), f"регион не поменялся на {options['region_remote']}"
            assert partner_new != partner_current, "список партнеров не поменялся"
            assert options[
                       'region_remote'] in user.get_page_title(), f"в заголовке страницы отсутствует  {options['region_remote']}"
            assert options[
                       'region_remote_link'] in user.get_current_url(), f" url не содержит правильной региональной части {options['region_remote_link']}"

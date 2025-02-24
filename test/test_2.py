from pages.sbis import Sbis


class TestRegionContacts:
    """
    Проверяет корректность формирования раздела контактов для региона по умолчанию и при выборе целевого региона
    """

    def test_default_region_contacts(self, browser, options):
        """
        Тестируем формирование раздела контактов для региона по умолчанию
        """
        user = Sbis(browser, options['delay'])
        user.get(options['url_sbis'])
        user.open_contacts_menu()
        user.goto_contacts_page()
        assert options['region_local'] == user.get_region_name(), f"регион по умолчанию не {options['region_local']}"
        assert user.get_partners(), "список партнеров отсутствует"

    def test_region_change(self, browser, options):
        """
        Проверяем корректность формирование раздела контактов при изменении региона по умолчанию на целевой регион
        """
        user = Sbis(browser, options['delay'])
        partner_current = user.get_partners()
        user.choice_region_menu(options['region_remote'])
        partner_new = user.get_partners()
        assert options['region_remote'] == user.get_region_name(), f"регион не поменялся на {options['region_remote']}"
        assert partner_new != partner_current, "список партнеров не поменялся"
        assert options[
                   'region_remote'] in user.get_page_title(), f"в заголовке страницы отсутствует  {options['region_remote']}"
        assert options[
                   'region_remote_link'] in user.get_current_url(), f" url не содержит правильной региональной части {options['region_remote_link']}"

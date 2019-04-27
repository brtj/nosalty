from requests_html import HTMLSession
import datetime


class scraper_nofluff:
    def url_get_data(self ,url):
        session = HTMLSession()
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15'}
        r = session.get(url, headers=headers)
        r.html.render(retries=3, wait=0.2, sleep=1, scrolldown=1, timeout=60)
        return r.html


    def url_get_categories_by_city(self, city):
        url_create = 'https://nofluffjobs.com/jobs/%s?criteria=city=%s' % (city, city)
        data = self.url_get_data(url_create)
        ads = data.find('#sticky-container', first=True)
        categories = []
        verify_string = '/jobs/%s' % city.lower()
        for category_url in ads.absolute_links:
            if verify_string in category_url:
                categories.append(category_url)
        return categories


    def url_get_offers(self, city, category):
        category_list = ['https://nofluffjobs.com/jobs/poznań/hr?criteria=city%253Dpozna%25C5%2584%20pozna%25C5%2584', 'https://nofluffjobs.com/jobs/poznań/frontend?criteria=city%253Dpozna%25C5%2584%20pozna%25C5%2584', 'https://nofluffjobs.com/jobs/poznań/devops?criteria=city%253Dpozna%25C5%2584%20pozna%25C5%2584', 'https://nofluffjobs.com/jobs/poznań/fullstack?criteria=city%253Dpozna%25C5%2584%20pozna%25C5%2584', 'https://nofluffjobs.com/jobs/poznań/backend?criteria=city%253Dpozna%25C5%2584%20pozna%25C5%2584', 'https://nofluffjobs.com/jobs/poznań/mobile?criteria=city%253Dpozna%25C5%2584%20pozna%25C5%2584', 'https://nofluffjobs.com/jobs/poznań/project-manager?criteria=city%253Dpozna%25C5%2584%20pozna%25C5%2584', 'https://nofluffjobs.com/jobs/poznań/support?criteria=city%253Dpozna%25C5%2584%20pozna%25C5%2584', 'https://nofluffjobs.com/jobs/poznań/testing?criteria=city%253Dpozna%25C5%2584%20pozna%25C5%2584', 'https://nofluffjobs.com/jobs/poznań/other?criteria=city%253Dpozna%25C5%2584%20pozna%25C5%2584'] #self.url_get_categories_by_city(city)
        for url in category_list:
            if category.lower() in url:
                return self.url_get_offers_list(url)


    def url_get_offers_list(self, url_category):
        data = self.url_get_data(url_category)
        offers = data.find('#sticky-container', first=True)
        offers_list = []
        verify_string = '/job/'
        for url_offer in offers.absolute_links:
            if verify_string in url_offer:
                offers_list.append(url_offer)
        return offers_list


    def parse_noflufjob_offers_list(self, offers_list):
        for url_offer in offers_list:
            self.parse_nofluffjob_offer(url_offer)

        '''sd
        parsowanie listy
        data parsowania listy | miasto | ilosc ogloszen_lacznie | min wynagrodzenie | srednie | mediana | max

        kolejna baza parsowanie listy
        data parsowania listy | miasto | kategoria | ilosc ogloszen_kategorii | min wynagrodzenie | srednie | mediana | max
        '''


    def parse_nofluffjob_offer(self, url):
        print(url)
        data = self.url_get_data(url)
        offer = data.find('#sticky-container', first=True)
        timestamp = self.current_date()
        vacancy_name = self.parse_get_field(offer, '.article-header-container', 'h1')
        company_name = self.parse_get_field(offer, '.dl-horizontal', 'dd')
        salary_uop, salary_b2b = self.parse_get_salary(offer)
        print(timestamp)
        print('Vacancy name: %s' % vacancy_name)
        print('Company name: %s' % company_name)
        print('Salary UoP: %s' % salary_uop)
        print('Salary B2B: %s' % salary_b2b)
        '''
        parsowanie oferty
        data parsowania | lokalizacja | nazwa firmy | rozmiar_firmy |  seniority | wynagrodzenie min b2b | wyn max b2b | wyn UoP min | wyn UoP max |
        wymagania lista |
        return json
        '''

    def current_date(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')


    def parse_get_field(self, data, htmlclass, htmlelement, id=None):
        field_name = data.find(htmlclass, first=True)
        field_find = field_name.find(htmlelement, first=True)
        return field_find.text


    def parse_get_salary(self, data):
        field_name = data.find('.essentials-desktop,.essentials-section', first=True)
        salary_text = field_name.text
        remove_list = ['Refer a friend', 'Apply Recommend a friend', '\n']
        for remove_string in remove_list:
            if remove_string in salary_text:
                salary_text = salary_text.replace(remove_string,'')
        salary_uop = None
        salary_b2b = None
        uop_string = '(UoP) per'
        b2b_string = '(B2B) per'
        uop_exist = False
        b2b_exist = False
        find_uop = None
        find_b2b = None
        if uop_string in salary_text:
            find_uop = salary_text.find(uop_string)
            uop_exist = True
        if b2b_string in salary_text:
            find_b2b = salary_text.find(b2b_string)
            b2b_exist = True

        if uop_exist:
            if find_b2b == None:
                salary_uop = salary_text[:find_uop]
            else:
                if find_uop < find_b2b:
                    salary_uop = salary_text[:find_uop]
                else:
                    b2b_first = find_b2b + len(b2b_string)
                    salary_uop = salary_text[b2b_first:find_uop]
                    for x in range(10):
                        if not salary_uop[:1].isdigit():
                            salary_uop = salary_uop[1:]
                        else:
                            pass

        if b2b_exist:
            if find_uop == None:
                salary_b2b = salary_text[:find_b2b]
            else:
                if find_b2b < find_uop:
                    salary_b2b = salary_text[:find_b2b]
                else:
                    uop_first = find_uop + len(uop_string)
                    salary_b2b = salary_text[uop_first:find_b2b]
                    for x in range(10):
                        if not salary_b2b[:1].isdigit():
                            salary_b2b = salary_b2b[1:]
                        else:
                            pass
        return salary_uop, salary_b2b


def main():
    scraper = scraper_nofluff()
    offers_list = scraper.url_get_offers('Poznań', 'DevOps')
    #offers_list = ['https://nofluffjobs.com/job/backend-developer-nova-tracking-lnpyozha?criteria=category%253Dbackend%20city%253Dpozna%25C5%2584%20pozna%25C5%2584','https://nofluffjobs.com/job/software-engineer-magnetar-rafal-suszka-xg1zpwls?criteria=category%253Dbackend%20city%253Dpozna%25C5%2584%20pozna%25C5%2584','https://nofluffjobs.com/job/senior-net-developer-next-it-poland-6e75navj?criteria=category%253Dbackend%20city%253Dpozna%25C5%2584%20pozna%25C5%2584','https://nofluffjobs.com/job/site-reliability-engineer-holidaycheck-l3gk0uef?criteria=category%253Ddevops%20city%253Dpozna%25C5%2584%20pozna%25C5%2584']
    scraper.parse_noflufjob_offers_list(offers_list)



if __name__ == "__main__":
    main()

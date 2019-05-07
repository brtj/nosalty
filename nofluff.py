#!/usr/bin/env python3
from requests_html import HTMLSession
import datetime
import re
import json
import logging
import argparse
import configparser
import requests
from collections import namedtuple
import logging.config


with open('logging.yaml', 'rt') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def parserinfo():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('--city', help='City name', required=True)
    required.add_argument('--category', help='Category', required=True)
    optional.add_argument('--optional_arg')
    args = parser.parse_args()
    return args


class scraper_nofluff:
    def configinfo(self):
        config = configparser.ConfigParser()
        config.read('config')
        if 'nofluffscraper' in config:
            noconf = namedtuple('config', ['retries', 'wait', 'sleep', 'scrolldown', 'timeout', 'url', 'api_login',
                                           'api_pass'])
            nofluffconf = noconf(config['nofluffscraper']['retries'],
                                 config['nofluffscraper']['wait'],
                                 config['nofluffscraper']['sleep'],
                                 config['nofluffscraper']['scrolldown'],
                                 config['nofluffscraper']['timeout'],
                                 config['django-server']['url'],
                                 config['django-server']['api_login'],
                                 config['django-server']['api_pass'])
            return nofluffconf
        else:
            raise ValueError('No config file created. Should be in script dir. Use config.template')


    def url_get_data(self ,url):
        config = self.configinfo()
        logging.info('Getting data for url: %s' % url)
        session = HTMLSession()
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15'}
        r = session.get(url, headers=headers)
        r.html.render(retries=int(config.retries), wait=int(config.wait), sleep=int(config.sleep),
                      scrolldown=int(config.scrolldown), timeout=int(config.timeout))
        return r.html


    def url_get_categories_by_city(self, city):
        url_create = 'https://nofluffjobs.com/jobs/%s?criteria=city=%s' % (city, city)
        logging.info('Getting categories for city: %s - url: %s' % (city,url_create))
        data = self.url_get_data(url_create)
        ads = data.find('#sticky-container', first=True)
        categories = []
        verify_string = '/jobs/%s' % city.lower()
        for category_url in ads.absolute_links:
            if verify_string in category_url:
                categories.append(category_url)
        logging.info('Categories for %s --- %s ' % (city, categories))
        return categories


    def url_get_offers(self, city, category):
        logging.info('Getting offers list for category %s in city %s.' % (category, city))
        category_list = self.url_get_categories_by_city(city)
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


    def parse_noflufjob_offers_list(self, offers_list, city, category):
        logging.info('Parsing %s offers from %s in category: %s' % (len(offers_list), city, category))
        timestamp = self.current_date()
        data = {'timestamp': timestamp, 'city': city, 'category': category, 'offers_count': len(offers_list)}
        for url_offer in offers_list:
            self.parse_nofluffjob_offer(url_offer, city, category)


    def parse_nofluffjob_offer(self, url, city, category):
        logging.info('Parsing offer - url: %s, city: %s, category: %s' % (url, city, category))
        data = self.url_get_data(url)
        offer = data.find('#sticky-container', first=True)
        timestamp = self.current_date()
        vacancy_name = self.parse_get_field(offer, '.article-header-container', 'h1')
        company_name = self.parse_get_field(offer, '.dl-horizontal', 'dd')
        salary_uop_min, salary_uop_max, salary_b2b_min, salary_b2b_max = self.parse_get_salary(offer)
        data = {'timestamp': timestamp, 'vacancy_name': vacancy_name, 'company_name': company_name,
                        'city':city, 'category': category,
                        'salary_uop_min':salary_uop_min, 'salary_uop_max': salary_uop_max, 'salary_b2b_min': salary_b2b_min,
                        'salary_b2b_max': salary_b2b_max}
        json_data = json.dumps(data)
        self.send_to_API(data)

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
        salary_uop_min = None
        salary_uop_max = None
        salary_b2b_min = None
        salary_b2b_max = None
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
            salary_uop_min, salary_uop_max = self.salary_uop_lowhigh(salary_uop)

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
            salary_b2b_min, salary_b2b_max = self.salary_b2b_lowhigh(salary_b2b)
        return salary_uop_min, salary_uop_max, salary_b2b_min, salary_b2b_max


    def salary_uop_lowhigh(self, salary_uop):
        isrange = salary_uop.find('-')
        if isrange == -1:
            salary_uop_low = self.salary_output_full(salary_uop)
            return salary_uop_low, salary_uop_low
        else:
            salary_split = salary_uop.split('-')
            salary_uop_low = self.salary_output_full(salary_split[0])
            salary_uop_high = self.salary_output_full(salary_split[1])
            return salary_uop_low, salary_uop_high


    def salary_b2b_lowhigh(self, salary_b2b):
        isrange = salary_b2b.find('-')
        if isrange == -1:
            salary_b2b_low = self.salary_output_full(salary_b2b)
            return salary_b2b_low, salary_b2b_low
        else:
            ismonthly = salary_b2b.find('K')
            # keep it mind it can be also hourly but didn't saw yet ///
            if ismonthly == -1:
                salary_split = salary_b2b.split('-')
                lowday = re.sub('[^0-9]', '', salary_split[0])
                highday = re.sub('[^0-9]', '', salary_split[1])
                salary_b2b_low = int(float(lowday) * 21)
                salary_b2b_high = int(float(highday) * 21)
                return salary_b2b_low, salary_b2b_high
            else:
                salary_split = salary_b2b.split('-')
                salary_b2b_low = self.salary_output_full(salary_split[0])
                salary_b2b_high = self.salary_output_full(salary_split[1])
                return salary_b2b_low, salary_b2b_high


    def salary_output_full(self, salary):
        salary_digit = re.sub('[^0-9.]', '', salary)
        salary = int(float(salary_digit) * 1000)
        return salary


    def send_to_API(self, json):
        try:
            config = self.configinfo()
            logging.info('Sending json to server')
            login = config.api_login
            password = config.api_pass
            url = config.url
            s = requests.Session()
            s.auth = (login, password)
            data = s.post(url, json=json)
            logging.info('Response: %s, data: %s' % (data.status_code, data.text))
        except Exception as e:
            print('--------------------- ERROR ---------------------')
            logging.exception('Error: %s' % e, exc_info=True)


def main():
    scraper = scraper_nofluff()
    args = parserinfo()
    logging.info('-------------- START SCRIPT for %s, %s --------------' % (args.city, args.category))
    scraper.configinfo()
    offers_list = scraper.url_get_offers(args.city, args.category)
    scraper.parse_noflufjob_offers_list(offers_list, args.city, args.category)
    logging.info('-------------- END SCRIPT for %s, %s --------------' % (args.city, args.category))



if __name__ == "__main__":
    main()

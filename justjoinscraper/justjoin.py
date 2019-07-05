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
import yaml


with open('logging.yaml', 'rt') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def parserinfo():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument('--category', help='Category', required=True)
    optional.add_argument('--optional_arg')
    args = parser.parse_args()
    return args


class scraper_justjoin:
    def configinfo(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        if 'justjoinscraper' in config:
            noconf = namedtuple('config', ['retries', 'wait', 'sleep', 'sleepcategory', 'scrolldown', 'timeout',
                                           'url_auth', 'url', 'api_login', 'api_pass'])
            nofluffconf = noconf(config['justjoinscraper']['retries'],
                                 config['justjoinscraper']['wait'],
                                 config['justjoinscraper']['sleep'],
                                 config['justjoinscraper']['sleepcategory'],
                                 config['justjoinscraper']['scrolldown'],
                                 config['justjoinscraper']['timeout'],
                                 config['django-server']['url_auth'],
                                 config['django-server']['url'],
                                 config['django-server']['api_login'],
                                 config['django-server']['api_pass'])
            return nofluffconf
        else:
            raise ValueError('No config file created. Should be in script dir. Use config.template')

    # categories are hardened and used in other scrapers. nofluff was first and thats all
    def url_get_categories(self):
        # hardened_categories = ['project-manager', https://justjoin.it/poznan/pm
        #                        'ux', https://justjoin.it/poznan/ux
        #                        'frontend', https://justjoin.it/poznan/javascript
        #                        'mobile', https://justjoin.it/poznan/mobile
        #                        'testing', https://justjoin.it/poznan/testing
        #                        'devops', https://justjoin.it/poznan/devops
        #                        'backend', https://justjoin.it/poznan/java, https://justjoin.it/poznan/python
        #                        'other', https://justjoin.it/poznan/other
        #                        ]
        hardened_categories = ['project-manager',
                               'ux',
                               'frontend',
                               'mobile',
                               'testing',
                               'devops',
                               'backend',
                               'other'
                               ]
        categories = []
        for category in hardened_categories:
            category_url = 'https://justjoin.it/all/%s' % (category.lower())
            categories.append(category_url)
        return categories


    # 1st - get categories
    def url_get_offers(self, category):
        logging.info('Getting offers list for category %s.' % (category))
        category_list = self.url_get_categories()
        for url in category_list:
            if category.lower() in url:
                return self.url_get_offers_list(url)


    # 2nd - get offers list - all ads for specific category
    def url_get_offers_list(self, url_category):
        url_category = 'https://justjoin.it/all/devops'
        data = self.url_get_data_category(url_category)
        field_name = data.find('.offers-list', first=True)
        offers = field_name.links
        offers_list = []
        logging.info('Getting %s offers for category %s' % (len(offers), url_category))
        verify_string = '/offers/'
        for url_offer in offers:
            if verify_string in url_offer:
                abs_link = 'https://justjoin.it'+url_offer
                offers_list.append(abs_link)
            if len(offers_list) == 0:
                logging.info('Offers list is EMPTY. URL: %s' % url_category)
        logging.info('-------------- OFFERS GATHERED --------------')
        logging.info(offers_list)
        logging.info('---------------------------------------------')
        return offers_list
        # offers_lista = ['https://justjoin.it/offers/egnyte-poland-network-engineer']
        # return offers_lista

    def url_get_data_category(self ,url):
        config = self.configinfo()
        logging.info('Getting data for url: %s' % url)
        session = HTMLSession()
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15'}
        r = session.get(url, headers=headers)
        r.html.render(retries=int(config.retries), wait=int(config.wait), sleep=int(config.sleepcategory),
                      scrolldown=int(config.scrolldown), timeout=int(config.timeout))
        return r.html


    # 3rd - parse offers_list
    def parse_justjoin_offers_list(self, offers_list, category):
        try:
            logging.info('Parsing %s offers in category: %s' % (len(offers_list), category))
            for url_offer in offers_list:
                self.parse_nofluffjob_offer(url_offer, category)
        except:
            logging.warning('No offers to PARSE. Offers list is EMPTY in category %s.' % (category))


    # 4th - parse offer and send to API
    def parse_nofluffjob_offer(self, url, category):
        logging.info('Parsing offer - url: %s, category: %s' % (url, category))
        data = self.url_get_data_offer(url)
        offer = data.find('.offer-details', first=True)
        timestamp = self.current_date()
        vacancy_name = self.parse_get_field(offer, '.offer-title-row', 'div')
        company_name = self.parse_get_field(offer, '.company-name', 'div')
        company_name_string = company_name.split('\n')[1]
        city = self.parse_get_field(offer, '.offer-address', 'div')
        city_string = city.split(',')[-1].strip()
        characters_list = [('ń', 'n'), ('ą', 'a'), ('ł', 'l'), ('ó', 'o'), ('ź', 'z')]
        for character in characters_list:
            if character[0] in city_string:
                city_replace = city_string.replace(character[0], character[1])
                city_string = city_replace
        salary_uop_min, salary_uop_max, salary_b2b_min, salary_b2b_max = self.parse_get_salary(offer)
        data = {'timestamp': timestamp, 'vacancy_name': vacancy_name, 'company_name': company_name_string,
                        'city':city_string.capitalize(), 'category': category.capitalize(),
                        'salary_uop_min':salary_uop_min, 'salary_uop_max': salary_uop_max, 'salary_b2b_min': salary_b2b_min,
                        'salary_b2b_max': salary_b2b_max, 'url_to_offer': url}
        json_data = json.dumps(data)
        print(json_data)
        self.send_to_API(data)


    def url_get_data_offer(self ,url):
        config = self.configinfo()
        logging.info('Getting data for url: %s' % url)
        session = HTMLSession()
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15'}
        r = session.get(url, headers=headers)
        r.html.render(retries=int(config.retries), wait=int(config.wait), sleep=int(config.sleep),
                      scrolldown=int(config.scrolldown), timeout=int(config.timeout))
        return r.html


    def parse_get_salary(self, data):
        field_name = data.find('.salary-row', first=True)
        salary_text = field_name.text
        print(salary_text)
        uop_string = 'gross/month'
        b2b_string = 'net/month'
        salary_uop_min = None
        salary_uop_max = None
        salary_b2b_min = None
        salary_b2b_max = None
        if uop_string in salary_text:
            salary_split = salary_text.split('-')
            salary_uop_min, salary_uop_max = self.salary_lowhigh(salary_split)
        if b2b_string in salary_text:
            salary_split = salary_text.split('-')
            salary_b2b_min, salary_b2b_max = self.salary_lowhigh(salary_split)
        return salary_uop_min, salary_uop_max, salary_b2b_min, salary_b2b_max

    def salary_lowhigh(self, salary_split):
        min = ''.join(salary_split[0].split())
        max = ''.join(salary_split[1].split())
        max_onlydigits = re.sub("[^0-9]", "", max)
        return min, max_onlydigits


    def current_date(self):
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')


    def parse_get_field(self, data, htmlclass, htmlelement, id=None):
        field_name = data.find(htmlclass, first=True)
        field_find = field_name.find(htmlelement, first=True)
        return field_find.text


    def send_to_API(self, json):
        try:
            config = self.configinfo()
            logging.info('Sending JSON to API, city: %s, company: %s, vacancy: %s' % (
                json['city'],
                json['company_name'],
                json['vacancy_name'])
            )
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


    def auth_to_API(self):
        config = self.configinfo()
        login = config.api_login
        password = config.api_pass
        url = config.url_auth
        s = requests.Session()
        s.auth = (login, password)
        data = s.get(url)
        if data.status_code != 200:
            logging.exception('Error: %s' % data.status_code)
            exit(1)


def main():
    scraper = scraper_justjoin()
    args = parserinfo()
    scraper.auth_to_API()
    logging.info('-------------- START SCRIPT for %s --------------' % (args.category))
    scraper.configinfo()
    offers_list = scraper.url_get_offers(args.category)
    scraper.parse_justjoin_offers_list(offers_list, args.category)
    logging.info('-------------- END SCRIPT for %s --------------' % (args.category))


if __name__ == "__main__":
    main()

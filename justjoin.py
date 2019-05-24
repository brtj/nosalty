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
    required.add_argument('--city', help='City name', required=True)
    required.add_argument('--category', help='Category', required=True)
    optional.add_argument('--optional_arg')
    args = parser.parse_args()
    return args


class scraper_justjoin:
    def configinfo(self):
        config = configparser.ConfigParser()
        config.read('config')
        if 'nofluffscraper' in config:
            noconf = namedtuple('config', ['retries', 'wait', 'sleep', 'sleepcategory', 'scrolldown', 'timeout', 'url', 'api_login',
                                           'api_pass'])
            nofluffconf = noconf(config['justjoinscraper']['retries'],
                                 config['justjoinscraper']['wait'],
                                 config['justjoinscraper']['sleep'],
                                 config['justjoinscraper']['sleepcategory'],
                                 config['justjoinscraper']['scrolldown'],
                                 config['justjoinscraper']['timeout'],
                                 config['django-server']['url'],
                                 config['django-server']['api_login'],
                                 config['django-server']['api_pass'])
            return nofluffconf
        else:
            raise ValueError('No config file created. Should be in script dir. Use config.template')


    def url_get_offers(self, city, category):
        # scrap offers for category e.g.
        # https://justjoin.it/poznan/devops
        # return proper offers_list


    def parse_justjoin_offers_list(self, offers_list, city, category):
        # parse offers list and send it to server


def main():
    scraper = scraper_justjoin()
    args = parserinfo()
    logging.info('-------------- START SCRIPT for %s, %s --------------' % (args.city, args.category))
    scraper.configinfo()
    offers_list = scraper.url_get_offers(args.city, args.category)
    scraper.parse_noflufjob_offers_list(offers_list, args.city, args.category)
    logging.info('-------------- END SCRIPT for %s, %s --------------' % (args.city, args.category))


if __name__ == "__main__":
    main()

    # hardened_categories = ['business-intelligence', https://justjoin.it/poznan/devops
    #                        'business-analyst', https://justjoin.it/poznan/devops
    #                        'support', https://justjoin.it/poznan/devops
    #                        'project-manager', https://justjoin.it/poznan/devops
    #                        'hr', https://justjoin.it/poznan/devops
    #                        'ux', https://justjoin.it/poznan/devops
    #                        'fullstack', https://justjoin.it/poznan/devops
    #                        'frontend', https://justjoin.it/poznan/devops
    #                        'mobile', https://justjoin.it/poznan/devops
    #                        'testing', https://justjoin.it/poznan/devops
    #                        'devops', https://justjoin.it/poznan/devops
    #                        'backend', https://justjoin.it/poznan/devops
    #                        ]

from selenium import webdriver

import requests
import re
import scrapy

from scrapy.loader import ItemLoader
from scraper.settings import USERNAME, PASSWORD
from scraper.items import Client
from nameparser import HumanName
from datetime import datetime


class ClientSpider(scrapy.Spider):
    name = "client"
    total_pages = 280
    url = 'https://felipeandsons.resurva.com/account-admin/accounts/clients/'
    get_client_booking_url = 'https://felipeandsons.resurva.com/' +\
        '/index/client-profile'

    login_user = USERNAME
    login_password = PASSWORD

    def get_cookies(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)
        base_url = self.url
        driver.get(base_url)
        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys(self.login_user)
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys(self.login_password)
        driver.find_element_by_name("login").click()
        cookies = driver.get_cookies()
        driver.close()
        return cookies

    def start_requests(self):
        for page in range(0, self.total_pages):
            yield scrapy.Request(url=self.url + '?page=' + str(page),
                                 callback=self.after_login,
                                 cookies=self.get_cookies())

    def after_login(self, response):
        user_ids = []
        for li in response.css('ul#clients-listing > li'):
            last_date_booking = li.css(
                'div.media-body > h4.media-heading > small').extract_first()
            # extract data in <small> tag
            date = re.search(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}',
                             last_date_booking).group(0)

            user_ids.append(
                {
                    'id': li.css('li > div.head::attr(class)')
                    .extract_first().split()[2].split('-')[1],
                    'date': datetime.strptime(date, '%Y-%m-%d')
                }
            )

        # Get users cookies
        jar = requests.cookies.RequestsCookieJar()
        for cookie in self.get_cookies():
            jar.set(cookie['name'], cookie['value'],
                    domain=cookie['domain'], path=cookie['path'])

        # Request users data
        for user in user_ids:
            r = requests.get(self.get_client_booking_url,
                             params={'id': user['id']}, cookies=jar)
            data = r.json()
            pdata = {}
            if type(data['bookings']) == dict:
                pdata =\
                    data['bookings'][list(data['bookings'].keys())[0]]
            else:
                pdata = data['bookings'][0]

            # Parse Full Name into parts
            name = HumanName(pdata['name'])

            client = ItemLoader(item=Client(), response=response)
            client.add_value('id', user['id'])
            client.add_value('last_booking_date', user['date'])
            client.add_value('first_name', name.first)
            client.add_value('last_name', name.last)
            client.add_value('email', pdata['email_address'])
            client.add_value('phone_number', pdata['phone_number'])

            yield client.load_item()

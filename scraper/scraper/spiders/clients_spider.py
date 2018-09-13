from selenium import webdriver

import requests
import scrapy

from scrapy.loader import ItemLoader
from scraper.items import Client


class ClientSpider(scrapy.Spider):
    name = "client"

    url = 'https://business101.resurva.com/account-admin/accounts/clients/'
    get_client_booking_url = 'https://business101.resurva.com/' +\
        '/index/client-profile'

    login_user = 'edwin@baseup.co'
    login_password = 'skudd1993'

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
        yield scrapy.Request(url=self.url,
                             callback=self.after_login,
                             cookies=self.get_cookies())

    def after_login(self, response):
        user_ids = []
        for li in response.css('ul#clients-listing > li'):
            user_ids.append(li.css('li > div::attr(class)')
                    .extract_first().split()[2].split('-')[1])

        # Get users cookies
        jar = requests.cookies.RequestsCookieJar()
        for cookie in self.get_cookies():
            jar.set(cookie['name'], cookie['value'],
                    domain=cookie['domain'], path=cookie['path'])

        # Request users data
        r = requests.get(self.get_client_booking_url,
                         params={'id': user_ids[0]}, cookies=jar)
        # data = r.json()

        # client = ItemLoader(item=Client(), response=response)
        # client.add_value('id', data['id'])
        # client.add_value('first_name', data['first_name'])
        # client.add_value('last_name', data['last_name'])

        # return client.load_item()
        self.logger.info(r.json())
        return r.json()

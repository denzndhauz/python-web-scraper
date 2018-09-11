import scrapy
from selenium import webdriver

class ClientSpider(scrapy.Spider):
    name = "client"

    url = 'https://business101.resurva.com/account-admin/accounts/clients/'
    login_url = 'https://business101.resurva.com/account-admin/accounts/clients/'
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
        yield scrapy.Request(url=self.url, callback=self.after_login, cookies=self.get_cookies())

    def after_login(self, response):
        for li in response.css('ul#clients-listing > li'):
            self.logger.info(li.xpath('//div[starts-with(@class, "head")]'));

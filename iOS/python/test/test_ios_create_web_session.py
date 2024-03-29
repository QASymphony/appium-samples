import unittest
import os
import copy
import sys

from time import sleep

from appium import webdriver
from helpers import IOS_BASE_CAPS, EXECUTOR
from selenium.common.exceptions import WebDriverException


class TestIOSCreateWebSession(unittest.TestCase):
    def test_should_create_and_destroy_ios_web_session(self):
        caps = copy.copy(IOS_BASE_CAPS)
        caps['name'] = self.id()
        # can only specify one of `app` and `browserName`
        caps['browserName'] = 'Safari'
        caps.pop('app')

        self.driver = webdriver.Remote(
            command_executor=EXECUTOR,
            desired_capabilities=caps
        )

        self.driver.get('https://www.google.com')
        assert 'Google' == self.driver.title

        self.driver.quit()

        sleep(5)

        with self.assertRaises(WebDriverException) as excinfo:
            self.driver.title
        self.assertTrue(
            'has already finished' in str(excinfo.exception.msg) or
            'Unhandled endpoint' in str(excinfo.exception.msg)
        )

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# --------------------------------
# | Author:   钱磊(Qian Lei)
# | Email:    qianlei90@gmail.com
# | Date:     2017-02-16 16:53:19
# | Version:  1.0
# --------------------------------
#

from time import sleep
from celery import Celery

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from config import AMAZON_URL, DEFAULT_SLEEP_TIME_IN_PAGE, DRIVER_TIMEOUT, MAX_PAGE_NUM
from utils.proxy import get_proxy
from utils.logger import logger

celery = Celery('tasks', broker='redis://localhost:6379/0')


def find_item(search_kw, target):
    proxy = get_proxy()
    logger.info(proxy)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={h}:{p}'.format(h=proxy[0], p=proxy[1]))
    chrome_options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images': 2})
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_page_load_timeout(DRIVER_TIMEOUT)

    try:
        driver.get(AMAZON_URL)
        e = driver.find_element_by_name('field-keywords')
        e.click()
        e.click()
        e.clear()
        e.send_keys(search_kw, Keys.RETURN)

        find_item = False
        page_num = 0
        while not find_item:
            page_num += 1
            if page_num >= MAX_PAGE_NUM:
                logger.error('超过{p}页仍未找到商品'.format(p=page_num))
                driver.close()
                return False

            try:
                e = driver.find_element_by_link_text(target)
            except NoSuchElementException as e:
                pass
            else:
                find_item = True

            if find_item:
                logger.info('第{page_num}页发现商品，进入页面'.format(page_num=page_num))
                driver.get(e.get_property('href'))
            else:
                logger.info('第{page_num}页未发现商品，进入下一页'.format(page_num=page_num))
                next_url = driver.find_element_by_id('pagnNextLink').get_property('href')
                driver.get(next_url)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);");
    except NoSuchElementException as e:
        logger.error('未找到数据')
        ret = False
    except TimeoutException as e:
        logger.error('访问超时')
        ret = False
    except Exception as e:
        logger.error(e)
        ret = False
    else:
        logger.info('等待{s}秒后完成任务'.format(s=DEFAULT_SLEEP_TIME_IN_PAGE))
        sleep(DEFAULT_SLEEP_TIME_IN_PAGE)
        ret = True
    finally:
        driver.close()
        return ret


@celery.task
def async_find_item(search_kw, target):
    find_item_ret = find_item(search_kw, target)
    while not find_item_ret:
        find_item_ret = find_item(search_kw, target)

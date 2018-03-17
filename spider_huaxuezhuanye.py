from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import sys
import io
import pymysql
import random
import csv
import re
import os
def get_medicine_name(path):  #读取中药材列表
    file = open(path, 'r')
    line = file.readlines()
    str_medicine = line[0]
    medicine_name = str_medicine.split(",")
    return  medicine_name
def get_load():
    browser.get(url)
    time.sleep(random.uniform(5, 6))
    try:
        username = browser.find_element_by_name('Username')
    except:
        fail_medicine.append(i)
    if (medicine_name.index(i) % 5 == 0):#循环使用五个账号
        username.send_keys('--')
    if (medicine_name.index(i) % 5 == 1):
        username.send_keys('--')
    if (medicine_name.index(i) % 5 == 2):
        username.send_keys('--')
    if (medicine_name.index(i) % 5 == 3):
        username.send_keys('--')
    if (medicine_name.index(i) % 5 == 4):
        username.send_keys('-')
    time.sleep(random.uniform(5, 6))
    try:
        password = browser.find_element_by_name('Password')
    except:
        fail_medicine.append(i)
    password.send_keys('--')
    time.sleep(random.uniform(5, 6))
    try:
        load = browser.find_element_by_name('login')
    except:
        fail_medicine.append(i)
    load.click()
    time.sleep(random.uniform(5, 6))
def get_search():#搜索中药材
    browser.get(url_search)#进入中药材搜索页面
    time.sleep(random.uniform(5, 6))
    try:
        name = browser.find_element_by_name('Specname')
    except:
        fail_medicine.append(i)
    name.send_keys(i)
    time.sleep(random.uniform(5, 6))
    try:
        search = browser.find_element_by_name('submit1')
    except:
        fail_medicine.append(i)
    search.click()
    time.sleep(random.uniform(5, 6))
def get_medicine():#获取中药材信息
    try:
        list_medicine = browser.find_elements_by_name('FID')
    except:
        fail_medicine.append(i)
    for j in range(len(list_medicine)):  # 遍历搜索结果
        try:
            list = browser.find_elements_by_name('FID')
        except:
            fail_medicine.append(i)
        list[j].click()  # 进入中药材信息结果界面
        time.sleep(random.uniform(20, 30))
        try:
            soup = BeautifulSoup(browser.page_source, 'html.parser')  # 获取中药材界面
            title = soup.find_all(attrs={'class': 'title_project1'})  # 获得中药材的目录
            content = soup.find_all(attrs={'class': 'content_project3'})  # 获得中药材的内容
        except:
            fail_medicine.append(i)
        for k in range(0, len(title)):
            if (title[k].text.strip() in dic_Chinese_medicine.keys()):
                dic_Chinese_medicine[title[k].text.strip()]=content[k].text.strip()
        try:
            reCount = cursor.execute(
                "insert into ChineseMedicine(Chinese_name,English_name,Latin_name,Medicine_sort,Medicine_description,Medicine_flavor,Pharmacology,Function_description,Function_effect,Medicine_meridian,Main_components,Biology_families,Biology_Chinese_name,Biology_Latin_name)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (dic_Chinese_medicine['中文名称'],dic_Chinese_medicine['英文名称'],dic_Chinese_medicine['拉丁文名'],dic_Chinese_medicine['药材类别'],dic_Chinese_medicine['药材描述'],dic_Chinese_medicine['药材性味'],dic_Chinese_medicine['药理作用'],dic_Chinese_medicine['功能描述'],dic_Chinese_medicine['功能作用'],dic_Chinese_medicine['药材归经'],dic_Chinese_medicine['主要成分'],dic_Chinese_medicine['生物科属'],dic_Chinese_medicine['生物中文名'],dic_Chinese_medicine['生物拉丁名']))
            conn.commit()  # 中药材信息入库
        except:
            fail_medicine.append(i)
        browser.back()
if __name__ == '__main__':
    medicine_name=get_medicine_name("C:/Users/Administrator/Desktop/我的文件/爬虫/数据样本/中药材/data_1.txt")
    conn = pymysql.connect(host="localhost", user="root", password="li123456789", db="huaxuezhuanye",
                           charset="utf8")  # 链接数据库
    cursor = conn.cursor()
    ChineseMedicine_insert = "insert into ChineseMedicine(Chinese_name,English_name,Latin_name,Medicine_sort,Medicine_description,Medicine_flavor,Pharmacology,Function_description,Function_effect,Medicine_meridian,Main_components,Biology_families,Biology_Chinese_name,Biology_Latin_name)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    url = 'http://www.organchem.csdb.cn/scdb/default.asp'
    url_search = 'http://www.organchem.csdb.cn/scdb/Tcm_Multi/q_tcd.asp'
    fail_medicine = []#记录未找到的中药材
    for i in medicine_name:
        browser = webdriver.Chrome()
        get_load()
        get_search()
        dic_Chinese_medicine ={'中文名称':'','英文名称':'','拉丁文名':'','药材类别':'','药材描述':'','药材性味':'','药理作用':'','功能描述':'','功能作用':'','药材归经':'','主要成分':'','生物科属':'','生物中文名':'','生物拉丁名':''}
        get_medicine()
        browser.quit()
    cursor.close()
    conn.close()
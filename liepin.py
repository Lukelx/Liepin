# _*_ coding: utf-8 _*_

import requests
from lxml import etree
import os
import time
import datetime
import csv

class Spider:
    def __init__(self, base_url, page_num, keyword, headers):
        self.base_url = base_url
        self.page_num = page_num + 1
        self.headers = headers
        self.keyword = keyword
        self.responses = []

    def crawler(self):
        for num in range(0, self.page_num):
            cur_url = self.base_url + f'?init=-1&dqs=020&key={self.keyword}&d_pageSize=40&curPage={num}'
            cur_response = requests.get(cur_url, headers=self.headers)
            cur_response.encoding = 'utf8'
            self.responses.append(cur_response)
            time.sleep(1)


class Parser:
    def __init__(self, responses):
        self.responses = responses
        self.jobs = []

    def parse(self):
        for response in self.responses:
            html = etree.HTML(response.text)
            job_names = html.xpath('//div[@class="job-info"]/span/a/text()')
            job_links = html.xpath('//div[@class="job-info"]/span/a/@href')
            job_dates = html.xpath('//div[@class="job-info"]/p[@class="time-info clearfix"]/time/@title')

            for n, l, d in zip(job_names, job_links, job_dates):
                cell = {
                    'title': n,
                    'link': l,
                    'date': d
                }
                self.jobs.append(cell)
                # [{}, {}]


class JobSave:
    def __init__(self, jobs):
        self.jobs = jobs
        self.job_sort()

        # [{}, {}] sorts
    def job_sort(self):
        jobs_sorted = sorted(self.jobs, key=lambda j: j['date'], reverse=True)
        return jobs_sorted

    def save_csv(self):
        jobs_save = self.job_sort()
        file_name = './' + str(datetime.date.today()) + '.csv'
        for j in jobs_save:
            with open(file_name, 'a', newline='', encoding='utf8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(j.keys())
                writer.writerow(j.values())
                writer.writerow('')


liepin_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.liepin.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
lp_keyword = 'python爬虫'
lp_base_url = 'https://www.liepin.com/sh/zhaopin/'

lp_spider = Spider(base_url=lp_base_url, page_num=1, keyword=lp_keyword, headers=liepin_headers)
lp_spider.crawler()
lp_parser = Parser(responses=lp_spider.responses)
lp_parser.parse()
lp_jobs = JobSave(jobs=lp_parser.jobs)
lp_jobs.save_csv()
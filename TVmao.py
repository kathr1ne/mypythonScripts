# coding:utf-8

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
import time
import requests
import datetime
import xlwt
# import chardet
import sys
import codecs


class Cctv:
    def __init__(self, homeUrl, name):
        self.homeUrl = homeUrl
        # profile = webdriver.FirefoxProfile()
        # profile.set_preference('network.proxy.type',1)
        # profile.set_preference('network.proxy.http','171.39.234.38')
        # profile.set_preference('network.proxy.http_port',80)
        # profile.update_preferences()
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
        #cap["phantomjs.page.settings.resourceTimeout"] = 20000
        cap["phantomjs.page.settings.loadImages"] = False
        # cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
        # self.browser = webdriver.PhantomJS(desired_capabilities=cap)
        self.proxy_address = '60.13.74.183:83'
        self.proxy_type = 'http'
        service_args = [
            '--proxy=%s' % self.proxy_address,
            '--proxy-type=%s' % self.proxy_type,
            #'--proxy-auth=ch01:Gf5TrfOi'
        ]
        self.browser = webdriver.PhantomJS(service_args=service_args, desired_capabilities=cap)
        self.browser.set_page_load_timeout(15)
        self.browser.set_script_timeout(15)
        self.epgInfo = []
        self.baseurl = "http://www.tvmao.com"
        self.basename = name
        self.pageSource = []
        self.nextDay = datetime.date.today() #+ datetime.timedelta(days=1)

    def close(self):
        self.browser.close()

    def get_program_info(self):
        self.get_page_source()
        for ps in self.pageSource:
            pl = self.get_epg_info(ps)
            if len(pl) > 0:
                self.epgInfo.append(pl)  # all epg
        if len(self.epgInfo) == 0:
            return
        for i in range(len(self.epgInfo) - 1):
            epg = self.epgInfo[i]
            self.epgInfo[i][len(epg) - 1]["endtime"] = self.epgInfo[i + 1][0]["starttime"]

    def get_page_source(self):
        self.nextDay = time.strftime("%Y.%m.%d")
        day_of_week = datetime.datetime.today().weekday() + 1
        for i in range(7):
            try:
                url = self.homeUrl % (day_of_week + i)
                self.browser.get(url)
            except TimeoutException:
                print "Url %s loading timeout, Stop loading!" % url
                self.browser.execute_script("window.stop()")
            #print self.browser.page_source
            self.pageSource.append(self.browser.page_source)

    def get_epg_info(self, html):
        programList = []  # one day epg
        soup = BeautifulSoup(html, 'lxml')
        day = self.get_date(soup)
        if not day:
            return []
        day = "2017-" + day
        time_struct = time.strptime(day, "%Y-%m-%d")
        day = time.strftime("%Y.%m.%d", time_struct)

        for li in soup.find('ul', id='pgrow').children:
            if isinstance(li, NavigableString):
                continue
            program = {}
            for info in li.children:
                if isinstance(info, NavigableString):
                    continue
                try:
                    time_and_name_class_name = info['class'][0]
                except KeyError:
                    print "Key Error!"
                    continue
                if time_and_name_class_name == "over_hide":
                    time_and_name = info.get_text()
                    if time_and_name:
                        time_and_name = time_and_name.strip()
                    else:
                        continue
                    desc_url = info.a
                    if desc_url:
                        desc_url = desc_url["href"]
                        desc_url = self.baseurl+desc_url
                        desc = self.get_description(desc_url)
                    else:
                        desc = ""

                    start_time = day + " " + time_and_name[0:5] + ":00"
                    program_name = time_and_name[5:].strip()

                    program["name"] = program_name
                    program["starttime"] = start_time
                    program["desc"] = desc
                    programList.append(program)
        if len(programList) == 0:
            return []
        for i in range(len(programList) - 1):
            programList[i]["endtime"] = programList[i + 1]["starttime"]
        programList[len(programList) - 1]["endtime"] = ''
        return programList

    def get_description(self, url):
        desc = ''
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
                  'Host': 'www.tvmao.com'}
        html = requests.get(url, headers=headers, proxies={self.proxy_type: "http://" + self.proxy_address}).content
        reg = re.compile(r'<div class="clear more_c".*?<p>(.*?)</p>', re.S)
        r = reg.search(html)
        if r:
            desc = r.group(1)
        return desc

    def get_date(self, soup):
        date_element = soup.select(".weekcur")
        day = ""
        if date_element:
            day = date_element[0].span.string
        return day

    def output_excel(self):
        print len(self.epgInfo)
        if len(self.epgInfo) == 0:
            return
        workbook = xlwt.Workbook(encoding="utf-8", style_compression=2)
        sheet = workbook.add_sheet("epg", cell_overwrite_ok=True)
        head = ["预告名称", "开始时间", "结束时间", "系统录制文件保存天数", "是否允许系统录制", "TVOD计费方式", "TVOD计费单位", " ", "是否允许个人录制", "个人录制计费方式",
                "个人计费单位", "个人录制价格", "预告简介"]
        for i in range(len(head)):
            sheet.write(0, i, head[i], self.set_style("head"))

        index = 1
        for epg in self.epgInfo:
            for program in epg:
                sheet.write(index, 0, program["name"], self.set_style("body"))
                sheet.write(index, 1, program["starttime"], self.set_style("body"))
                sheet.write(index, 2, program["endtime"], self.set_style("body"))
                sheet.write(index, 3, "3", self.set_style("body"))
                sheet.write(index, 4, "1", self.set_style("body"))
                sheet.write(index, 5, "0", self.set_style("body"))
                sheet.write(index, 6, "1", self.set_style("body"))
                sheet.write(index, 7, "0", self.set_style("body"))
                sheet.write(index, 8, "0", self.set_style("body"))
                sheet.write(index, 9, "0", self.set_style("body"))
                sheet.write(index, 10, "0", self.set_style("body"))
                sheet.write(index, 11, "0", self.set_style("body"))
                sheet.write(index, 12, program["desc"], self.set_style("body"))
                index += 1

        workbook.save(self.basename + ".xls")

    def set_style(self, t):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        if t == "head":
            font.name = "Time New Roman"
            font.height = 220
            font.bold = True
            font.color_index = 4
        elif t == "body":
            font.name = "Time New Roman"
            font.height = 220
            font.bold = False
            font.color_index = 4
        style.font = font
        return style


def start_run(url, name):
    cctv3 = Cctv(url, name)
    print "Starting parse %s ......" % url
    try:
        cctv3.get_program_info()
    except Exception as e:
        print e
    cctv3.close()
    print "Starting write to excel ......"
    cctv3.output_excel()
    print "parsing EPG OK!"


def main():
    urlList = ['http://www.tvmao.com/program_satellite/BTV1-w%d.html', 'http://www.tvmao.com/program_satellite/HUNANTV1-w%d.html',
               'http://www.tvmao.com/program/CHC-CHC1-w%d.html','http://www.tvmao.com/program/CCTV-CCTV8-w%d.html',
               'http://www.tvmao.com/program_satellite/DONGFANG1-w%d.html','http://www.tvmao.com/program/GDTV-GDTV1-w%d.html',
               'http://www.tvmao.com/program/SZTV-SZTV1-w%d.html','http://www.tvmao.com/program/CHC-CHC2-w%d.html',
               'http://www.tvmao.com/program/CHC-CHC3-w%d.html','http://www.tvmao.com/program/CCTV-CCTV3-w%d.html',
               'http://www.tvmao.com/program/CCTV-CCTV5-w%d.html','http://www.tvmao.com/program/CCTV-CCTV6-w%d.html',
               'http://www.tvmao.com/program_satellite/ZJTV1-w%d.html','http://www.tvmao.com/program/PHOENIX-PHOENIX1-w%d.html',
               'http://www.tvmao.com/program/PHOENIX-PHOENIXHK-w%d.html','http://www.tvmao.com/program/PHOENIX-PHOENIX-INFONEWS-w%d.html',
               'http://www.tvmao.com/program/BBC-BBC-KNOWLEDGE-ASIA-w%d.html', 'http://www.tvmao.com/program/BBC-BBC-ENTERTAINMENT-ASIA-w%d.html',
               'http://www.tvmao.com/program/BBC-BBC-LIFESTYLE-ASIA-w%d.html','http://www.tvmao.com/program/BBC-BBC-CBEEBIES-ASIA-w%d.html',
               'http://www.tvmao.com/program/CARTON-BOOMERANG-w%d.html', 'http://www.tvmao.com/program/CARTON-CARTOON-HK-w%d.html',
               'http://www.tvmao.com/program/CARTON-CARTOON-SG-w%d.html','http://www.tvmao.com/program/CARTON-CARTOON-TW-w%d.html',
               'http://www.tvmao.com/program/CNN-CNN1-w%d.html','http://www.tvmao.com/program/DISNEY-DISNEY-SG-w%d.html',
               'http://www.tvmao.com/program/DISNEY-DISNEY-HK-w%d.html','http://www.tvmao.com/program/DISNEY-DISNEY-TW-w%d.html',
               'http://www.tvmao.com/program/DISNEY-DISNEY-JUNIOR-SG-w%d.html','http://www.tvmao.com/program/DISNEY-DISNEY-JUNIOR-TW-w%d.html',
               'http://www.tvmao.com/program/DISNEY-DISNEY-XD-SG-w%d.html','http://www.tvmao.com/program/NOWTV-TOONAMI-w%d.html']
    nameList = ['Beijing TV','Hunan TV','CHC Action(H265)','CCTV 8','Dongfang TV','Guangdong TV','Shenzhen TV','CHC Family(H265)','CHC HD(H265)','CCTV 3','CCTV 5','CCTV 6','Zhejiang',
                'Phx Chinese HD(H265)','Phx HK HD(H265)','Phx Infonews HD(H265)', 'BBC Earth Asia(H265)', 'BBC Entertainment Asia(H265)',
                'BBC Lifestyle Asia', 'BBC CBeeBies HD(H265)', 'Boomerang Australia', 'Cartoon Network P(H265)', 'Cartoon Network S E A(H265)',
                'Cartoon Network Taiwan(H265)', 'CNN International Asia Pacific(H265)', 'Disney Channel Asia(H265)', 'Disney Channel Hong Kong(H265)',
                'Disney Channel Taiwan(H265)', 'Disney Junior Asia(H265)', 'Disney Junior Taiwan(H265)', 'Disney XD Asia(H265)', 'Toonami(H265)']

    # urlList = ['http://www.tvmao.com/program/CHC-CHC1-w%d.html']
    # nameList = ['CHC Action']

    if len(sys.argv) > 1:
        try:
            name = sys.argv[1]
            index = nameList.index(name)
            url = urlList[index]
            start_run(url, name)
        except ValueError, IndexError:
            print "channel name error!"
    else:
        for i in range(len(urlList)):
            url = urlList[i]
            name = nameList[i]
            start_run(url, name)

if __name__ == "__main__":
    s = time.time()
    main()
    print time.time()-s

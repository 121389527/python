import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import json
def get_page(url):
    try:
        headers = {
            "Referer":"http://www.weather.com.cn/forecast/",
            "UserAgent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.content.decode('utf-8')
        return None
    except RequestException:
        return None

def parse_page(html):
    soup = BeautifulSoup(html,'lxml')
    conMidtab = soup.find('div',class_='conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):   #enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:                
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]   #将生成器转化为列表
            temp_td = tds[-5]
            max_temp = list(temp_td.stripped_strings)[0]
            yield {
                "city":city,
                "max_temp":max_temp
            }

def write_to_file(content):
    with open ('weather.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main():
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml#',
        'http://www.weather.com.cn/textFC/db.shtml#',
        'http://www.weather.com.cn/textFC/hd.shtml#',
        'http://www.weather.com.cn/textFC/hz.shtml#',
        'http://www.weather.com.cn/textFC/hn.shtml#',
        'http://www.weather.com.cn/textFC/xb.shtml#',
        'http://www.weather.com.cn/textFC/xn.shtml#'
    ]
    for url in urls:
        html = get_page(url)
        for weather in parse_page(html):
            write_to_file(weather)

if __name__ == "__main__":
    main()

'''
问题1：第三个tr标签中，第一个td标签为省份，第二个td标签才为城市，
       而余下tr标签中，第一个td标签为城市，在爬取过程中应对此进行区分
'''
import requests
from requests.exceptions import RequestException
from lxml import etree
import json


def get_one_page(url):
    try:
        headers = {
            "UserAgent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        }
        response = requests.get(url,headers=headers)
        if response.status_code ==200:
            return response.text
        return None
    except RequestException:
        return None

def parse_page(html):
    tree = etree.HTML(html)
    ol = tree.xpath("//ol[@class='grid_view']")[0]
    lis = ol.xpath("./li")
    for li in lis:
        try:
            title = li.xpath(".//span[@class='title']/text()")[0]
            score = li.xpath(".//span[@class='rating_num' and @property='v:average']/text()")[0]
            quote = li.xpath(".//span[@class='inq']/text()")[0]
            yield {
                "title":title,
                "score":score,
                "quote":quote
            }
        except:
            return None

def write_to_file(content):
    with open ('movies.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main():
    for i in range(10):
        url = 'https://movie.douban.com/top250?start={}&filter='.format(i*25)
        html = get_one_page(url) 
        for movie in parse_page(html):
            write_to_file(movie)

if __name__ == "__main__":
    main()



'''
问题1：第180条电影没有quote,程序直接跳过该页剩余信息，爬取下一页怎么处理？
'''
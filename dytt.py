import requests
from requests.exceptions import RequestException
from lxml import etree
import json
import pymongo


def get_page(url):
    try:
        headers = {
            "Referer":"https://www.dytt8.net/",
            "UserAgent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.content
        return None
    except RequestException:
        return None

def parse_page(html):
    base_url = 'https://www.dytt8.net'
    tree = etree.HTML(html)
    detail_urls = tree.xpath("//table[@class='tbspan']//a/@href")
    detail_urls = map(lambda url:base_url + url,detail_urls)
    return detail_urls

def parse_detail_page(detail_url):
    movie = {}
    html = get_page(detail_url)
    tree = etree.HTML(html)
    title = tree.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    movie['title'] = title
    
    zoom = tree.xpath("//div[@id='Zoom']")[0]
    imgs = zoom.xpath(".//img/@src")
    cover = imgs[0]
    movie['cover'] = cover

    def parse_info(info,rule):
        return info.replace(rule,"").strip()  #strip() 去除空格等字符串
    infos = zoom.xpath(".//text()")  #直接用text()获取其内容
    for index,info in enumerate(infos):
        #print(info)
        if info.startswith("◎年　　代"):
            info = parse_info(info,"◎年　　代")
            movie['year'] = info
        elif info.startswith("◎产　　地"):
            info = parse_info(info,"◎产　　地")
            movie['country'] = info
        elif info.startswith("◎类　　别"):
            info = parse_info(info,"◎类　　别")
            movie['category'] = info
        elif info.startswith("◎豆瓣评分"):
            info = parse_info(info,"◎豆瓣评分")
            movie['douban_rating'] = info
        elif info.startswith("◎导　　演"):
            info = parse_info(info,"◎导　　演")
            movie['director'] = info
        elif info.startswith("◎主　　演"):
            info = parse_info(info,"◎主　　演")
            actors = [info]
            for x in range(index+1,len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎"):
                    break
                actors.append(actor)
                movie['actors'] = actors
        elif info.startswith("◎简　　介"):
            info = parse_info(info,"◎简　　介")
            for x in range(index+1,len(infos)):
                profile = infos[x]
            if profile.startswith("【下载地址】"):
                profile = info(x).strip()
                movie["profile"] = profile
    downlaod_url = tree.xpath("//td[@bgcolor='#fdfddf']/a/@href")[0]
    movie["download_url"] = downlaod_url
    return movie

def write_to_file(content):
    with open ('dytt.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

def main():
    movies = []
    bsae_url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    for i in range(1,8):
        # 第一个for循环用来控制总共有7页
        url = bsae_url.format(i)
        html = get_page(url)
        detail_urls = parse_page(html)
        for detail_url in detail_urls:
            #第二个for循环用来遍历一页电影中所有电影的详情url
            movie = parse_detail_page(detail_url)
            movies.append(movie)
            write_to_file(movies)

if __name__ == "__main__":
    main()
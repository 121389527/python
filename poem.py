import requests
from requests.exceptions import RequestException
import re
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
    title_pattern = re.compile('<div class="sons">.*?<b>(.*?)</b>.*?</div>',re.S)
    titles = re.findall(title_pattern,html)
    dynasty_pattern = re.compile('<p class="source">.*?target="_blank">(.*?)</a>.*?</div>',re.S)
    dynasties = re.findall(dynasty_pattern,html)
    author_pattern = re.compile('<p class="source">.*?</span>.*?target="_blank">(.*?)</a>.*?</div>',re.S)
    authors = re.findall(author_pattern,html) 
    content_pattern = re.compile('<div class="contson".*?>(.*?)</div>',re.S)
    contents_tag = re.findall(content_pattern,html)
    contents = []
    for content in contents_tag:
        x = re.sub(r'<.*?>','',content)
        contents.append(x.strip()) 
    poems = []
    #zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
    for value in zip(titles,dynasties,authors,contents):  
        title,dynasty,author,content = value
        poem = {
            'title':title,
            'dynasty':dynasty,
            'author':author,
            'content':content
        }
        poems.append(poem)
    for poem in poems:
        with open ('poems.txt','a',encoding='utf-8') as f:
            f.write(json.dumps(poem,ensure_ascii=False)+'\n')

def main():
    for i in range(1,11):
        url = "https://www.gushiwen.org/default.aspx?page={}".format(i)
        html = get_one_page(url)
        parse_page(html)

if __name__ == "__main__":
    main()
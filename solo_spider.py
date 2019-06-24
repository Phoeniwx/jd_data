# coding=utf-8
from asyncio import sleep
import requests
import re
import json
import random
import pandas as pd

comments_tab = pd.DataFrame(columns=['id', 'content', 'time', 'usefulVoteCount',
                                     'uselessVoteCount', 'productColor', 'productSize', 'score'])

user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


def get_one_page(page, score, id_num):
    # 爬取一页评论，每页10条，page为页号，score为星级（0-5，0表示所有）
    s = requests.Session()
    header = {
        'Referer': 'http://item.jd.com/' + id_num + '.html',
        'Sec-Fetch-Mode': 'no-cors',
        'User-Agent': random.choice(user_agents)
    }
    data = {
        'callback': 'fetchJSON_comment98vv3085',
        'productId': id_num,
        'score': score,
        'sortType': 5,
        'page': page,
        'pageSize': 10,
        'isShadowSku': 0,
        'rid': 0,
        'fold': 1
    }
    print('爬取页面：' + str(page + 1))
    try:
        r = s.get('http://sclub.jd.com/comment/skuProductPageComments.action', params=data,
                  headers=header)
        # print(r.text)
        t = re.search(r'(?<=fetchJSON_comment98vv3085\().*(?=\);)', r.text).group(0)
    except Exception as e:
        print(e)
        return 1
    # print(r.text)
    j = json.loads(t)
    f = open('out.json', 'w')
    with f:
        json.dump(j, f, indent=4, ensure_ascii=False)
        # f.write(r.text)
        f.write('\n')
    comments = j['comments']
    print(j['maxPage'])
    global comments_tab
    for comment in comments:
        comments_tab = comments_tab.append(pd.DataFrame({'id': [comment['id']],
                                                         'content': [comment['content']],
                                                         'time': [comment['creationTime']],
                                                         'usefulVoteCount': [comment['usefulVoteCount']],
                                                         'uselessVoteCount': [comment['uselessVoteCount']],
                                                         'productColor': [comment['productColor']],
                                                         'productSize': [comment['productSize']],
                                                         'score': [comment['score']]}), ignore_index=True)
    return 0


if __name__ == '__main__':
    items = ['100000287141', '100000177758', '100000177760', '100000177756',
             '100000287115', '100000177826', '100000287121', '100000177782',
             '100000177802', '100000177788', '100000177770', '100000177776',
             '100000177766', '100000287163', '100000287165']
    # 爬取100页差评（1000条）
    for i in items:
        for j in range(3):
            while get_one_page(1, j+1, i) == 1:
                # 限制爬取频率
                sleep(random.randint(1, 9))

    # 储存到csv文件，注意每次储存会覆盖
    # comments_tab.to_csv('bad_comments.csv')

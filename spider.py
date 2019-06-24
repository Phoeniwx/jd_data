# coding=utf-8
from asyncio import sleep
from http import cookiejar
import requests
import re
import json
import random
import threading
import pandas as pd


class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False


lock = threading.Lock()

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


def get_one_page(page, score, proxy, item_id):
    global lock
    url = 'http://club.jd.com/comment/skuProductPageComments.action'
    s = requests.Session()
    s.keep_alive = False
    s.cookies.set_policy(BlockAll())
    header = {
        'Referer': 'http://item.jd.com/' + item_id + '.html',
        'Sec-Fetch-Mode': 'no-cors',
        'User-Agent': random.choice(user_agents)
    }
    data = {
        'callback': 'fetchJSON_comment98vv3085',
        'productId': item_id,
        'score': score,
        'sortType': 5,
        'page': page,
        'pageSize': 10,
        'isShadowSku': 0,
        'rid': 0,
        'fold': 1
    }
    print(item_id + '-' + str(score) + ' 爬取页面：' + str(page + 1))
    try:
        # proxies = requests.get("http://localhost:4567/get/20").json()
        r = s.get(url, params=data,
                  headers=header, proxies=proxy)
        # print(r.text)
        t = re.search(r'(?<=fetchJSON_comment98vv3085\().*(?=\);)', r.text).group(0)
    except Exception as e:
        # print(e)
        return 1
    # print(r.text)
    j = json.loads(t)
    comments = j['comments']
    if comments:
        with lock:
            f = open('iPhone XR/' + str(score) + '_out.txt', 'a')
            with f:
                # json.dump(j, f, indent=4, ensure_ascii=False)
                f.write(r.text)
                f.write('\n')
    else:
        return 2
    global comments_tab
    for comment in comments:
        df = pd.DataFrame({'id': [comment['id']],
                           'content': [comment['content']],
                           'time': [comment['creationTime']],
                           'usefulVoteCount': [comment['usefulVoteCount']],
                           'uselessVoteCount': [comment['uselessVoteCount']],
                           'productName': [comment['referenceName']],
                           'productColor': [comment['productColor']],
                           'productSize': [comment['productSize']],
                           'score': [comment['score']]})
        with lock:
            add_records('iPhone XR/' + str(score) + '_com.csv', df)
            # comments_tab = comments_tab.append(df, ignore_index=True)
    return 0


def add_records(csv, df):
    df.to_csv(csv, mode='a', header=False)


def sub_thread(start, score, item_id):
    global lock
    with lock:
        proxy = requests.get("http://localhost:4567/pop").json()
    for i in range(5):
        r = get_one_page(start + i, score, proxy, item_id)
        if r == 1:
            with lock:
                proxy = requests.get("http://localhost:4567/pop").json()
            get_one_page(start + i, score, proxy, item_id)
        elif r == 2:
            return
        else:
            pass
        sleep(random.randint(1, 5))
    return


if __name__ == '__main__':
    items = ['100000287141', '100000177758', '100000177760', '100000177756',
             '100000287115', '100000177826', '100000287121', '100000177782',
             '100000177802', '100000177788', '100000177770', '100000177776',
             '100000177766', '100000287163', '100000287165']

    for num in items:
        for j in range(3):
            print('Crawling ' + num + ' Score: ' + str(j+1))
            threads = [threading.Thread(target=sub_thread, args=(i * 5, j+1, num)) for i in range(20)]
            [thr.start() for thr in threads]
            [thr.join(timeout=6) for thr in threads]

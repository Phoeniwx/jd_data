import re
import json
import pandas as pd

comments_tab = pd.DataFrame(columns=['id', 'content', 'time', 'usefulVoteCount',
                                     'uselessVoteCount', 'productName', 'productColor', 'productSize', 'score'])


def txt_process():
    global comments_tab
    with open('medium_out.txt') as f:
        line = f.readline()
        i = 1
        while line:
            print(i)
            i = i + 1
            t = re.search(r'(?<=fetchJSON_comment98vv3085\().*(?=\);)', line).group(0)
            if t:
                j = json.loads(t)
                comments = j['comments']
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
                    comments_tab = comments_tab.append(df, ignore_index=True)
            line = f.readline()
    comments_tab.to_csv('m_com.csv')


def csv_process():
    global comments_tab
    for i in range(3):
        df = pd.read_csv('iPhone XR/' + str(i+1) + '_com.csv', header=None, index_col=0, names=['id', 'content',
                                                                                 'time', 'usefulVoteCount', 'uselessVoteCount', 'productName', 'productColor', 'productSize', 'score'])
        comments_tab = comments_tab.append(df, ignore_index=True)
    print(comments_tab.head(5))
    comments_tab.to_csv('iPhone XR/' + 'all_comments.csv')


if __name__ == '__main__':
    csv_process()

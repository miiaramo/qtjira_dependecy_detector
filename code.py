import json
import re
import pandas as pd
from collections import defaultdict

ISSUEPATTERN = re.compile(r'((QBS|QTBUG|QTWB)-[0-9]{1,5})')


def get_data():
    f = open('QBS-UPC_input.json', 'r', encoding="utf8")
    data = json.loads(f.read(), encoding="utf8")
    f.close()
    return data


def get_links(data):
    links = data['dependencies']
    dependencies = pd.DataFrame(columns=['fromid', 'toid', 'dependency_type', 'created_at'], data=[[l['fromid'], l['toid'], l['dependency_type'], l['created_at']] for l in links])
    return dependencies


def get_comments_with_links(data):
    requirements = []
    for requirement in data['requirements']:
        for comment in requirement['comments']:
            ids = re.findall(ISSUEPATTERN, comment['text'])
            if len(ids) > 0:
                for toid in ids:
                    requirements.append([requirement['id'], toid[0], comment['text'], comment['created_at']])

    return pd.DataFrame(columns=['fromid', 'toid', 'comments', 'created_at'], data=requirements)


def get_labeled(links, comments):
    return pd.merge(links, comments, on=['fromid', 'toid'], how='inner')


def get_proposed(data):
    proposed = []
    found = 0
    for requirement in data['requirements']:
        for comment in requirement['comments']:
            ids = re.findall(ISSUEPATTERN, comment['text'])
            if len(ids) > 0:
                for dependency in data['dependencies']:
                    if dependency['fromid'] == requirement['id']:
                        for id in ids:
                            if id[0] == dependency['toid']:
                                fromid = dependency['fromid']
                                toid = dependency['toid']
                                dependency_type = dependency['dependency_type']
                                comment_text = comment['text']
                for toid in ids:
                    fromid = requirement['id']
                    dep = {
                        "id": '_'.join([fromid, toid[0], 'SIMILAR']),
                        "dependency_type": "similar",
                        "dependency_score": 1.0,
                        "status": "proposed",
                        "fromid": fromid,
                        "toid": toid[0],
                        "description": [
                            comment['text']
                        ],
                        "created_at": 0
                    }
                    proposed.append(dep)
    print(found)
    return proposed


def main():
    data = get_data()
    links = get_links(data)
    print(links)
    comments = get_comments_with_links(data)
    print(comments)
    labeled = get_labeled(links, comments)
    print(labeled[['dependency_type', 'comments']])
    # proposed = get_proposed(data)
    # for prop in proposed:
    #     print(prop)


if __name__ == '__main__':
    main()

import json
import re

ISSUEPATTERN = re.compile(r'((QBS|QTBUG|QTWB)-[0-9]{1,5})')
proposed = []


def download():
    f = open('QBS-UPC_input.json', 'r')
    data = json.loads(f.read())
    f.close()

    for requirement in data['requirements']:
        for comment in requirement['comments']:
            ids = re.findall(ISSUEPATTERN, comment['text'])
            if len(ids) > 0:
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
    print(proposed[0])


if __name__ == '__main__':
    download()

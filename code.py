import json
import re

FILE = 'QBS-UPC_input.json'
PROJECTS = 'QTSOLBUG|QTSYSADM|QTJIRA|QSR|QDS|QTVSADDINBUG|QTWEBSITE|AUTOSUITE|PYSIDE|QTCOMPONENTS|QTIFW|QBS|QTMOBILITY|QTQAINFRA|QT3DS|QTCREATORBUG|QTBUG|QTWB|QTPLAYGROUND'
ISSUEPATTERN = re.compile(r'(('+PROJECTS+')-[0-9]{1,5})')


def get_data():
    f = open(FILE, 'r', encoding='utf8')
    data = json.loads(f.read(), encoding='utf8')
    f.close()
    return data


def get_proposed(data):
    proposed = []
    for requirement in data['requirements']:
        for comment in requirement['comments']:
            ids = re.findall(ISSUEPATTERN, comment['text'])
            if len(ids) > 0:
                for toid in ids:
                    fromid = requirement['id']
                    dep = {
                        'id': '_'.join([fromid, toid[0], 'SIMILAR']),
                        'dependency_type': 'similar',
                        'dependency_score': 1.0,
                        'status': 'proposed',
                        'fromid': fromid,
                        'toid': toid[0],
                        'description': [
                            comment['text']
                        ],
                        'created_at': 0
                    }
                    proposed.append(dep)
    return proposed


def main():
    data = get_data()
    proposed = get_proposed(data)
    for prop in proposed:
        print(prop)


if __name__ == '__main__':
    main()

import json
import re

ISSUEPATTERN = re.compile(r'((QBS|QTBUG|QTWB)-[0-9]{1,5})')


def get_data():
  f = open('QBS-UPC_input.json', 'r')
  data = json.loads(f.read())
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
  return proposed


def main():
  data = get_data()
  proposed = get_proposed(data)


if __name__ == '__main__':
  main()
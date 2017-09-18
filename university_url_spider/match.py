import sys
import json


def match(name0, name1):
    if name0 == name1:
        return True
    elif '（' in name0 or '（' in name1:
        name0 = name0.replace('（', '(').replace('）', ')')
        name1 = name1.replace('（', '(').replace('）', ')')
        print(name0 + ": " + name1)
        return match(name0, name1)
    else:
        return False


def main(params):
    agency = open(params['agency']).readlines()
    url = json.loads(open(params['url']).read())
    match = open(params['match'], "a")
    err = open(params['error'], "a")
    not_match = open('warning.json', "a")

    result = {}
    error = dict(url)
    warning = list(agency)

    for item in url.keys():
        for agency in agency:
            if match(item, agency):
                result[agency] = url[item]
                warning.remove(agency)
                error.pop(item)

    print(len(result), len(error), len(warning))

    match.write(json.dumps(result, ensure_ascii=False))
    err.write(json.dumps(error, ensure_ascii=False))
    not_match.write(json.dumps(warning, ensure_ascii=False))


def fetch_params():
    params_list = ["agency", "url", "match", "error"]
    params = {
        "agency": "agency.txt",
        "url": "url.json",
        "match": "result.json",
        "error": "error.json",
    }
    for i in range(1, len(sys.argv)):
        params[params_list[i - 1]] = sys.argv[i]
    return params


if __name__ == '__main__':
    params = fetch_params()
    main(params)

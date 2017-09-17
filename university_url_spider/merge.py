import sys
import json


def print_items(dict):
    for item in dict.items():
        print(item)

def tran_list_to_dict(list):
    dict = {}
    for item in list:
        for key in item.keys():
            dict[key] = item[key]
    return dict

def merge(A, B):
    AandB = {}
    AexB = {}
    BexA = {}
    error = {}

    for key in A_dict.keys():
        if key in B_dict:
            if A_dict[key] in B_dict[key] or B_dict[key] in A_dict[key]:
                AandB[key] = A_dict[key]
            else:
                error[key] = {A_dict[key], B_dict[key]}
            B_dict.pop(key)
        else:
            AexB[key] = A_dict[key]

    for key in B_dict.keys():
        BexA[key] = B_dict[key]

    print(len(A_json), len(B_json))
    print(len(AandB), len(error))
    print(len(AexB), len(BexA))

    return [result, error]


def main():
    params_list = ["A_filename", "B_filename", "result_filename", "error_filename"]
    params = {
        "A_filename": "A.json",
        "B_filename": "B.json",
        "result_filename": "result.json", 
        "error_filename": "error.json", 
    }
    for i in range(1, len(sys.argv)):
        params[params_list[i-1]] = sys.argv[i]

    A = open(params['A_filename']).read()
    B = open(params['B_filename']).read()
    result = open(params_list['result_filename'], "a")
    error = open(params_list['error_filename'], "a")
    A_json = json.loads(A)
    B_json = json.loads(B)
    A_dict = tran_list_to_dict(A_json)
    B_dict = tran_list_to_dict(B_json)
    


if __name__ == '__main__':
    main()
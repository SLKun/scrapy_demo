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
    result = {}
    error = {}

    for key in A.keys():
        if key in B:
            if A[key] in B[key] or B[key] in A[key]:
                AandB[key] = A[key]
                result[key] = A[key]
            else:
                error[key] = {A[key], B[key]}
                result[key] = A[key]
            B.pop(key)
        else:
            AexB[key] = A[key]
            result[key] = A[key]

    for key in B.keys():
        BexA[key] = B[key]
        result[key] = B[key]

    print(len(AandB), len(error))
    print(len(AexB), len(BexA))
    print(len(result))

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
    result = open(params['result_filename'], "a")
    error = open(params['error_filename'], "a")
    A_json = json.loads(A)
    B_json = json.loads(B)
    A_dict = tran_list_to_dict(A_json)
    B_dict = tran_list_to_dict(B_json)
    print(len(A_dict), len(B_dict))
    [result_dict, error_dict] = merge(A_dict, B_dict)

    result.write(json.dumps(result_dict, ensure_ascii=False))
    # error.write(json.dumps(error_dict))
    print_items(error_dict)

if __name__ == '__main__':
    main()
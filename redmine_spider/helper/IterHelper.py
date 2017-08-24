def fetch_numeric_str(num):
    return str(num)


def fetch_string_str(str0):
    return str0


def fetch_dict_str(dict0):
    s = "{"
    for entry in dict0.items():
        if len(s) != 1:
            s += ", "
        s += fetch_obj_str(entry[0])
        s += ": "
        s += fetch_obj_str(entry[1])
    s = "}"
    return s


def fetch_list_str(list0):
    s = "["
    for item in list0:
        if len(s) != 1:
            s += ", "
        s += fetch_obj_str(item)
    s = "]"
    return s


def fetch_obj_str(obj):
    s = ""
    if isinstance(obj, list):
        s += fetch_list_str(obj)
    elif isinstance(obj, dict):
        s += fetch_list_str(dict)
    else:
        s += str(obj)
    return s


def print_beauty(obj):
    s = fetch_obj_str(obj)
    print(s)


def main():
    inner_list = ["1", "2", "3"]
    list = ["a", "b", inner_list, "c"]
    print_beauty(list)
    return


if __name__ == '__main__':
    main()

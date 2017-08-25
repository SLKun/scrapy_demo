global_indent = 0
indent_str = "    "


def fetch_string_str(str0):
    return "'" + str0 + "'"


def fetch_dict_str(dict0):
    global global_indent
    global_indent += 1
    s = "{"
    for entry in dict0.items():
        if len(s) != 1:
            s += ",\n" + global_indent * indent_str
        s += fetch_obj_str(entry[0])
        s += ": "
        s += fetch_obj_str(entry[1])
    s = "}"
    global_indent -= 1
    return s


def fetch_list_str(list0):
    global global_indent
    global_indent += 1
    s = "["
    isList = False
    for item in list0:
        if len(s) != 1:
            if isinstance(item, (dict, list)):
                s += ",\n" + global_indent * indent_str
                isList = True
            elif isList:
                s += ",\n "
                isList = False
            else:
                s += ", "
        s += fetch_obj_str(item)
    s += "]"
    global_indent -= 1
    return s


def fetch_obj_str(obj):
    s = ""
    if isinstance(obj, list):
        s += fetch_list_str(obj)
    elif isinstance(obj, dict):
        s += fetch_dict_str(obj)
    elif isinstance(obj, str):
        s += fetch_string_str(obj)
    else:
        s += str(obj)
    return s


def print_beauty(obj):
    s = fetch_obj_str(obj)
    print(s)
    print(obj)


def main():
    inner_list = ["1", "2", "3"]
    list = ["a", "b", inner_list, "c"]
    print_beauty(list)
    return


if __name__ == '__main__':
    main()
